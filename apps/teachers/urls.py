# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import TeacherIndexView, TeacherInfoShowView, TeacherInfoView, TeacherScoreInfoView, \
    TeacherScoreListView, TeacherStudentListView, TeacherStudentInfoView, TeacherClassListView

app_name = 'teachers'

urlpatterns = [

    url(r"^index/$", TeacherIndexView.as_view(), name='teacher_index'),

    url(r"^infoshow/$", TeacherInfoShowView.as_view(), name='teacher_infoshow'),

    url(r"^info/$", TeacherInfoView.as_view(), name='teacher_info'),

    url(r"^studentlist/$", TeacherStudentListView.as_view(), name='teacher_studentlist'),

    url(r"^studentinfo/$", TeacherStudentInfoView.as_view(), name='teacher_studentinfo'),

    url(r"^scorelist/$", TeacherScoreListView.as_view(), name='teacher_scorelist'),

    url(r"^scoreinfo/$", TeacherScoreInfoView.as_view(), name='teacher_scoreinfo'),

    url(r"^classlist/$", TeacherClassListView.as_view(), name='teacher_classlist'),


]
