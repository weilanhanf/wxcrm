# -*- coding: utf-8 -*-

from django import forms


class TeacherInfoViewForm(forms.Form):
    # 教师信息录入表达验证

    ID = forms.CharField(required=True, max_length=18, min_length=18)

