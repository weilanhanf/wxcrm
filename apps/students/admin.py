from django.contrib import admin

from .models import ScoreInfo, StudentInfo, ExamList

# Register your models here.

class ExamListAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['id', 'time']


class ScoreInfoAdmin(admin.ModelAdmin):
    list_per_page = 1000
    list_display = ['file_number', 'which_exam', 'get_student_class', 'get_student_grade',
                    'chinese', 'math', 'english', 'physical', 'chemistry', 'biology',
                    'politics', 'geography', 'history', 'sum_score', 'grade_rank', 'class_rank', 'remark']
    search_fields = ['file_number__student_name', 'which_exam__time', 'remark']
    list_filter = ['file_number', 'which_exam', 'file_number__grade', 'file_number__clas']

    # 课程列表页添加字段修改功能
    # list_editable = ['remark']
    # 设置只读字段
    # readonly_fields = ['file_number', 'which_exam', 'exam_number','chinese', 'math', 'english', 'physical', 'chemistry', 'biology', 'politics',
    #         'geography', 'history', 'remark']
    # 设置隐藏字段 与readonly_fields功能相冲突，一个字段只能使用二者之一

    exclude = ['sum_score', 'grade_rank', 'class_rank']
    show_bookmarks = False  # 去除标签功能


class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'teacher']
    list_per_page = 5

admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.register(ScoreInfo, ScoreInfoAdmin)
admin.site.register(ExamList, ExamListAdmin)
admin.site.unregister(ExamList)
admin.site.unregister(StudentInfo)
admin.site.unregister(ScoreInfo)