from django.contrib import admin

from .models import DormitoryInfo

# Register your models here.
class DormitoryInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['dormitory_number', 'year', 'teacher', 'get_student_number', 'get_dormitory_students', 'remark', ]
    # list_editable = ['remark']
    search_fields = ['teacher__name', 'dormitory_number']
    list_filter = ['year', 'teacher__name']
    show_bookmarks = False  # 去除标签功能

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)



admin.site.register(DormitoryInfo, DormitoryInfoAdmin)
admin.site.unregister(DormitoryInfo)