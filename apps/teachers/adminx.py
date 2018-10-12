# -*- coding: utf-8 -*-
import xadmin

from .models import TeacherInfo


class TeacherInfoAdmin(object):
    list_per_page = 10
    list_display = ['number', 'name', 'gender', 'is_class_leader', 'phone', 'email', 'subject' ]
    search_fields = ['name', 'ID', 'phone', 'remark', 'subject']
    list_filter = ['is_class_leader', 'gender']
    # list_editable = ['remark']

    show_bookmarks = False  # 去除标签功能


xadmin.site.register(TeacherInfo, TeacherInfoAdmin)
