# -*- coding: utf-8 -*-
from django.shortcuts import redirect, reverse

from students.models import StudentInfo
from teachers.models import TeacherInfo


class LoginRequiredMixin(object):
    # 做用户登录检查，如果未登录则返回登录首页
    def dispatch(self, request, *args, **kwargs):

        # 检测当前用户状态，如果is_login不为True，则跳转到登陆界面
        if request.session.get('is_login', None):

            # 在用户当前站点可能会修改url跳转到其他站点：如teacher/index-->student/index
            # 在调转之前通过session中的username检查过滤。如果不存在，返回登录界面
            ask_site = request.get_full_path()[1:8]
            # print(request.session.get('username'), request.get_full_path()[1:8])
            try:
                if ask_site == 'student':
                    StudentInfo.objects.get(file_number__exact=request.session.get('username'))
                elif ask_site == 'teacher':
                    TeacherInfo.objects.get(number__exact=request.session.get('username'))
            except:
                return redirect(reverse('login'))

            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
