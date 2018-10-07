# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import StudentInfoView, StudentScoreView, StudentIndexView

app_name = 'students'

urlpatterns = [
    # 学生站点首页
    url(r"^index/$", StudentIndexView.as_view(), name='student_index'),
    # 学生基本信息页
    url(r"^info/$", StudentInfoView.as_view(), name='student_info'),
    # 学生成绩列表
    url(r"^score/$", StudentScoreView.as_view(), name='student_score'),
]