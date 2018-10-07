# -*- coding: utf-8 -*-
import xadmin
from xadmin import views

from .models import Administrator, DormitoryInfo, EmailVerifyRecord, GradeInfo, ClassInfo


# class AdministratorAdmin(object):
#     pass


class DormitoryInfoAdmin(object):
    list_per_page = 10
    list_display = ['dormitory_number', 'year', 'teacher', 'get_student_number', 'get_dormitory_students', 'remark', ]
    list_editable = ['remark']
    search_fields = ['teacher__name', 'dormitory_number']
    list_filter = ['teacher', 'year', 'dormitory_number']
    unique_together = ['dormitory_number', 'year']
    show_bookmarks = False  # 去除标签功能


class EmailVerifyRecordAdmin(object):
    pass


class GradeInfoAdmin(object):
    list_editable = ['remark']
    list_display = ['grade_number', 'year', 'header', 'remark', 'get_class_number', 'get_grade_students_number', ]
    unique_together = ['year', 'grade_number']
    show_bookmarks = False  # 去除标签功能


class ClassInfoAdmin(object):
    list_per_page = 10
    list_display = ['class_number', 'grade', 'header', 'chinese_teacher', 'math_teacher', 'english_teacher',
                    'physical_teacher', 'chemistry_teacher', 'biology_teacher', 'politics_teacher', 'geography_teacher',
                    'history_teacher', 'sport_teacher', 'music_teacher', 'get_class_student_number', 'remark',]
    list_editable = ['remark']
    list_filter = ['class_number', 'grade', 'header', ]
    unique_together = ['year', 'class_number']
    search_fields = ['header_name', ]
    show_bookmarks = False  # 去除标签功能


xadmin.site.register(DormitoryInfo, DormitoryInfoAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.unregister(EmailVerifyRecord)
xadmin.site.register(ClassInfo, ClassInfoAdmin)
# xadmin.site.unregister(ClassInfo)
xadmin.site.register(GradeInfo, GradeInfoAdmin)
# xadmin.site.unregister(GradeInfo)
