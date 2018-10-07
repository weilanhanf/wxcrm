"""wxcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
import xadmin

from students.views import LogoutView, LoginView, RegisterView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    # 学生相关操作
    url(r"^student/", include("students.urls", namespace='student')),
    # 老师相关操作
    url(r"^teacher/", include("teachers.urls", namespace='teacher')),
    # 配置验证码相关
    url('captcha/', include('captcha.urls')),
]
