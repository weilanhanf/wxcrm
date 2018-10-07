# -*- coding: utf-8 -*-
import xadmin

from .models import TeacherInfo


class TeacherInfoAdmin(object):
    list_per_page = 10
    list_display = ['number', 'name', 'is_class_leader', 'phone', 'email', 'remark', 'get_student_number', ]
    search_fields = ['name', 'ID', 'phone', 'remark', 'subject']
    list_filter = ['is_class_leader', 'subject']
    list_editable = ['remark']
    show_bookmarks = False  # 去除标签功能


xadmin.site.register(TeacherInfo, TeacherInfoAdmin)
