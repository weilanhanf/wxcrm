from django.contrib import admin

from .models import ScoreInfo, StudentInfo, ExamList

# Register your models here.

class ExamListAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['id', 'time']


class ScoreInfoAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['exam_number', 'get_sum_score', 'get_class_rank']


class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'teacher']
    list_per_page = 5


admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.register(ScoreInfo, ScoreInfoAdmin)
admin.site.register(ExamList, ExamListAdmin)
admin.site.unregister(ExamList)
admin.site.unregister(StudentInfo)
admin.site.unregister(ScoreInfo)