from django.contrib import admin

from .models import TeacherInfo

# Register your models here.


class TeacherInfoAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['name', 'email', 'phone']


# class MyAdminSite(admin.AdminSite):
#     site_header = '好医生运维资源管理系统'  # 此处设置页面显示标题
#     site_title = '好医生运维'  # 此处设置页面头部标题


# admin_site = MyAdminSite(name='management')
admin.site.site_header = '好医生运维资源管理系统'
admin.site.site_title = '好医生运维'

admin.site.register(TeacherInfo, TeacherInfoAdmin)
admin.site.unregister(TeacherInfo)
