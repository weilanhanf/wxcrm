from django.contrib import admin

from .models import DormitoryInfo

# Register your models here.
class DormitoryInfoAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['dormitory_id', 'teacher', 'remark']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)



admin.site.register(DormitoryInfo, DormitoryInfoAdmin)
admin.site.unregister(DormitoryInfo)