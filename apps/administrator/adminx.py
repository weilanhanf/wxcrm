# -*- coding: utf-8 -*-
import xadmin

from .models import DormitoryInfo, EmailVerifyRecord, GradeInfo, ClassInfo


class AdministratorAdmin(object):
    show_bookmarks = False  # 去除标签功能


class DormitoryInfoAdmin(object):
    list_per_page = 10
    list_display = ['dormitory_number', 'year', 'teacher', 'get_student_number', 'get_dormitory_students', 'remark', ]
    # list_editable = ['remark']
    search_fields = ['teacher__name', 'dormitory_number']
    list_filter = ['year', ]
    show_bookmarks = False  # 去除标签功能


class EmailVerifyRecordAdmin(object):
    pass


class GradeInfoAdmin(object):
    # list_editable = ['remark']
    list_display = ['grade_number', 'year', 'header', 'get_class_number', 'get_grade_students_number', ]
    show_bookmarks = False  # 去除标签功能


class ClassInfoAdmin(object):
    list_per_page = 10
    list_display = ['class_number', 'grade', 'header', 'chinese_teacher', 'math_teacher', 'english_teacher',
                    'physical_teacher', 'chemistry_teacher', 'biology_teacher', 'politics_teacher', 'geography_teacher',
                    'history_teacher', 'sport_teacher', 'music_teacher', 'get_class_student_number', 'remark', ]
    # list_editable = ['remark']
    list_filter = ['class_number', 'grade', 'header', ]
    search_fields = ['header__name', ]
    show_bookmarks = False  # 去除标签功能


xadmin.site.register(DormitoryInfo, DormitoryInfoAdmin)
# xadmin.site.unregister(DormitoryInfo)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.unregister(EmailVerifyRecord)
xadmin.site.register(ClassInfo, ClassInfoAdmin)
# xadmin.site.unregister(ClassInfo)
xadmin.site.register(GradeInfo, GradeInfoAdmin)
# xadmin.site.unregister(GradeInfo)
