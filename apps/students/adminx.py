# -*- coding: utf-8 -*-
__date__ = '2018/9/23 17:30'

import xadmin
from xadmin import views

from xadmin.views.list import ListAdminView
from .models import ScoreInfo, StudentInfo, ExamList, RewardPunishInfo


class BaseSetting(object):
    enable_themes = True  # 使用主体功能
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "温县第一高级中学后台管理"  # 左上角
    site_footer = "welcome to 温县第一高级中学后台管理 如果有问题请联系：XXXXXXXXXXX"  # 底部
    menu_style = "accordion"  # 管理左侧菜单

    # def get_site_menu(self):
    #     return [
    #         {
    #             'title': '投票管理',
    #             'perm': self.get_model_perm(ScoreInfo, 'change'),
    #             'menus': (
    #                 {
    #                     'title': '投票',
    #                     'url': ''get_model_url(ScoreInfo, 'changelist')},
    #                 {
    #                     'title': '选票',
    #                     'url': 'www.baidu.com',
    #                     'icon': 'fa fa-user-md',
    #                     'perm': ''get_model_url(StudentInfo, 'changelist')},
    #             )
    #         },
    #     ]


class StudentInfoAdmin(object):
    list_per_page = 10
    list_display = ['file_number', 'student_name', 'teacher', 'gender', 'year_join', 'clas', 'grade', 'art_science', 'nation', 'dormitory_number', 'remark']
    search_fields = ['student_name', 'teacher__name']  # 保证在search_field这个容器类型中不存在整型，浮点型
    list_filter = ['teacher', 'clas', 'gender', 'art_science', 'grade', 'nation']
    show_bookmarks = False  # 去除标签功能

    # 课程列表页添加字段修改功能
    # list_editable = ['file_number', 'student_name', 'ID', 'gender', 'password', 'phone', 'teacher', 'year_join', 'grade', 'clas',
    #                 'art_science', 'nation', 'dormitory_number', 'bed_number', 'address', 'remark']
    # readonly_fields = ['file_number', 'student_name', 'ID', 'gender', 'password', 'phone', 'teacher', 'year_join', 'grade', 'clas',
    #                 'art_science', 'nation', 'dormitory_number', 'bed_number', 'address', 'remark']


class ScoreInfoAdmin(object):
    list_per_page = 10
    list_display = ['file_number', 'which_exam', 'get_student_class', 'get_student_grade',
                    'chinese', 'math', 'english', 'physical', 'chemistry', 'biology',
                    'politics', 'geography', 'history', 'sum_score', 'grade_rank', 'class_rank', 'remark']
    search_fields = ['file_number__student_name', 'which_exam__time', 'remark']
    list_filter = ['file_number', 'which_exam', 'file_number__grade', 'file_number__clas', 'file_number__teacher']
    # 课程列表页添加字段修改功能
    list_editable = ['remark']
    # 设置只读字段
    # readonly_fields = ['score_id']
    # 设置隐藏字段 与readonly_fields功能相冲突，一个字段只能使用二者之一
    exclude = ['sum_score', 'grade_rank', 'class_rank']
    show_bookmarks = False  # 去除标签功能

    actions = ['really_delete_selected']  # 增加删除行为

    def get_actions(self, request):
        actions = super(ScoreInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            # print(obj, self)
            # print(type(self).__mro__)

            # 更新班级排名
            exam_id = obj.which_exam.id  # 确定本次考试的ID
            grade = obj.file_number.grade  # 确定本次考试的年级
            clas = obj.file_number.clas  # 确定年级

            need_class_score_list = ScoreInfo.objects.filter(
                which_exam__id=exam_id,
                file_number__grade=grade,
                file_number__clas=clas,
                class_rank__gt=obj.class_rank
            )  # 需要班级排名+1的所有成绩记录的列表

            for score in need_class_score_list:  # 成绩记录排名逐个+1
                score.class_rank -= 1
                score.save()

            # 更新年级排名
            need_grade_score_list = ScoreInfo.objects.filter(
                which_exam__id=exam_id,
                file_number__grade=grade,
                grade_rank__gt=obj.grade_rank
            )  # 需要年级排名+1的所有成绩记录的列表

            for score in need_grade_score_list:  # 成绩记录排名逐个+1
                score.grade_rank -= 1
                score.save()

            obj.delete()
    really_delete_selected.short_description = " X 删除并更新排名"


class ExamListAdmin(object):
    list_per_page = 10
    list_display = ['id', 'time', 'remark']
    list_editable = ['remark']
    search_fields = ['remark', 'time']
    list_filter = ['id', 'time']
    show_bookmarks = False  # 去除标签功能


class RewardPunishInfoAdmin(object):
    list_per_page = 10
    list_display = ['student', 'reward_remark', 'get_reward_sum', 'punish_remark', 'get_punish_remark', ]
    search_fields = ['student__student_name', 'reward_remark', 'punish_remark']
    list_editable = ['reward_remark', 'punish_remark', ]
    list_filter = ['student', 'student__clas', 'student__grade']
    show_bookmarks = False  # 去除标签功能


xadmin.site.register(views.BaseAdminView, BaseSetting)
# 基本配置管理与views绑定
xadmin.site.register(views.CommAdminView, GlobalSettings)
# 将title和footer信息进行注册
xadmin.site.register(StudentInfo, StudentInfoAdmin)
xadmin.site.register(ScoreInfo, ScoreInfoAdmin)
xadmin.site.register(ExamList, ExamListAdmin)
xadmin.site.register(RewardPunishInfo, RewardPunishInfoAdmin)
# xadmin.site.unregister(RewardPunish)
