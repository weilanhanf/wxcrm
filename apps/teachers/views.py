from django.shortcuts import render, redirect, reverse
from django.views import View
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from .models import TeacherInfo
from administrator.models import GradeInfo, ClassInfo
from students.models import ExamList, StudentInfo, ScoreInfo

from django.core.exceptions import FieldError


class TeacherIndexView(LoginRequiredMixin, View):
    # 教师首页

    def get(self, request):
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)
        teacher_name = teacher.name
        context = {
            'title': '教师首页',
            'teacher_name': teacher_name
        }
        return render(request, 'teacher/teacher_index.html', context)


class TeacherInfoShowView(LoginRequiredMixin, View):
    # 教师基本信息页

    def get(self, request):

        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)
        success = request.GET.get('success')
        context = {
            'save_success': success,
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息'
        }
        return render(request, 'teacher/teacher_info_show.html', context)


class TeacherInfoView(LoginRequiredMixin, View):
    # 教师基本信息页

    def get(self, request):

        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)
        context = {
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息'
        }
        return render(request, 'teacher/teacher_info.html', context)

    def post(self, request):

        # 将get赋值为可调用的request.POST.get对象
        get = request.POST.get

        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        if get('is_class_leader') == 'on':  # 从表单获取的is_class_leader值为on str类型
            teacher.is_class_leader = True
        else:
            teacher.is_class_leader = False

        if get('gender') == 'male':
            teacher.gender = '男'
        else:
            teacher.gender = '女'

        # 数据库更新
        teacher.name, teacher.password, teacher.email, teacher.phone, \
        teacher.ID, teacher.subject, teacher.remark = get('name'), \
        get('password'), get('email'), get('phone'), get('ID'), get('subject'), get('remark')
        # print(get('remark'), teacher.remark)
        teacher.save()  # 保存到数据库

        return redirect(reverse('teacher:teacher_infoshow')+'?success=1')


class TeacherClassListView(LoginRequiredMixin, View):
    # 老师所教班级列表 先找出老师所教的班，然后在筛选

    def get(self, request):
        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        # 找出老师所教的班，只考虑老师当班主任或者当任课老师，不存在当班主任却教其他版的课
        if teacher.is_class_leader:
            class_queryset = teacher.classinfo_set.all()
        else:
            class_queryset = ClassInfo.objects.filter(
                Q(chinese_teacher__number__exact=teacher.number) |
                Q(math_teacher__number__exact=teacher.number) |
                Q(english_teacher__number__exact=teacher.number) |
                Q(physical_teacher__number__exact=teacher.number) |
                Q(chemistry_teacher__number__exact=teacher.number) |
                Q(biology_teacher__number__exact=teacher.number) |
                Q(politics_teacher__number__exact=teacher.number) |
                Q(geography_teacher__number__exact=teacher.number) |
                Q(history_teacher__number__exact=teacher.number) |
                Q(sport_teacher__number__exact=teacher.number) |
                Q(music_teacher__number__exact=teacher.number)
            )

        # 从前端获取筛选条件并放入列表中
        o_select_condition = request.GET.get('o')
        p_select_condition = request.GET.get('p')
        all_page_condition = request.GET.get('all')

        # 如果不为空,则放入同一个列表中
        select_condition_list = []
        if o_select_condition:
            select_condition_list.append(o_select_condition)
        if p_select_condition:
            select_condition_list.append(p_select_condition)

        # 强制类型转换去除重复条件
        select_condition_set = set(select_condition_list)
        select_condition_list = list(select_condition_set)

        # 利用筛选条件并通过外键关联查询老师当过班主任的班级
        try:
            select_condition_tuple = tuple(select_condition_list)  # 传入多个筛选条件
            class_queryset = class_queryset.order_by(*select_condition_tuple)
        except FieldError:
            class_queryset = class_queryset.all()

        # 过滤器
        grade_filter_condition = request.GET.get('grade_id')
        grade_queryset = GradeInfo.objects.all().order_by('-year')
        filter_condition_list = []
        if grade_filter_condition:
            class_queryset = class_queryset.filter(grade__id__exact=grade_filter_condition)
            filter_condition_list.append(grade_filter_condition)

        # 过滤器个数
        filter_count = len(filter_condition_list)

        # 搜索框
        q_search_condition = request.GET.get('q')
        if q_search_condition:
            class_queryset = class_queryset.filter(header__name__icontains=q_search_condition)

        # 获取筛选过的总数据量并传到前段
        class_queryset_count = len(class_queryset)

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        if all_page_condition and  class_queryset_count > 0:
            # 每一页显示几条数据 如果all=1则显示全部
            page_count = class_queryset_count
        else:
            page_count = 5
        p = Paginator(class_queryset, page_count, request=request)
        class_page = p.page(page)

        context = {
            'q': q_search_condition,
            'grade_id': grade_filter_condition,
            'filter_count': filter_count,
            'grade_queryset': grade_queryset,
            'p': p_select_condition,
            'o': o_select_condition,
            'all': all_page_condition,
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息',
            'class_page': class_page,
            'class_queryset_count': class_queryset_count
        }
        return render(request, 'teacher/teacher_classlist.html', context)


class TeacherStudentListView(LoginRequiredMixin, View):
    # 老师所教学生列表

    def get(self, request):

        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        # 找出老师所教的班，只考虑老师当班主任或者当任课老师，不存在当班主任却教其他版的课
        if teacher.is_class_leader:
            class_queryset = teacher.classinfo_set.all()
        else:
            class_queryset = ClassInfo.objects.filter(
             Q(chinese_teacher__number__exact=teacher.number) |
             Q(math_teacher__number__exact=teacher.number) |
             Q(english_teacher__number__exact=teacher.number) |
             Q(physical_teacher__number__exact=teacher.number) |
             Q(chemistry_teacher__number__exact=teacher.number) |
             Q(biology_teacher__number__exact=teacher.number) |
             Q(politics_teacher__number__exact=teacher.number) |
             Q(geography_teacher__number__exact=teacher.number) |
             Q(history_teacher__number__exact=teacher.number) |
             Q(sport_teacher__number__exact=teacher.number) |
             Q(music_teacher__number__exact=teacher.number)
        )

        # 根据班级的id反向查询所有的学生
        class_id_list = [clas_.id for clas_ in class_queryset]
        student_queryset = StudentInfo.objects.filter(clas__id__in=class_id_list).all()

        # 外键关联筛选
        rel_class_condition = request.GET.get('rel_clas__id')
        if rel_class_condition and rel_class_condition is not None:
            student_queryset = student_queryset.filter(clas_id__exact=int(rel_class_condition))

        # 从前端获取筛选条件
        all_page_condition = request.GET.get('all')
        clas_select_condition = request.GET.get('clas')
        year_join_select_condition = request.GET.get('year_join')
        grade_select_condition = request.GET.get('grade')

        # 如果不为空,则放入同一个列表中
        select_condition_list = [clas_select_condition, year_join_select_condition, grade_select_condition]

        # 强制类型转换去除重复条件
        order_condition_list = [condition for condition in select_condition_list if condition]  # 去杂
        select_condition_set = set(order_condition_list)
        select_condition_list = list(select_condition_set)
        # print(select_condition_list)

        # 利用排序条件并通过外键关联查询老师当过班主任的班级
        try:
            select_condition_tuple = tuple(select_condition_list)  # 传入多个排序条件
            student_queryset = student_queryset.order_by(*select_condition_tuple)
        except Exception:
            student_queryset = student_queryset.all()

        # 过滤器
        grade_queryset = GradeInfo.objects.all().order_by('-year')
        class_filter_queryset = class_queryset
        filter_condition_list = []
        grade_filter_condition = request.GET.get('grade_id')
        class_filter_condition = request.GET.get('class_id')
        art_science_filter_condition = request.GET.get('art_science')
        gender_filter_condition = request.GET.get('gender')


        # 过滤器筛选
        if grade_filter_condition and grade_filter_condition is not 'None':
            student_queryset = student_queryset.filter(grade_id__exact=int(grade_filter_condition))
            filter_condition_list.append(grade_filter_condition)
        if class_filter_condition and class_filter_condition is not 'None':
            student_queryset = student_queryset.filter(clas_id__exact=int(class_filter_condition))
            filter_condition_list.append(class_filter_condition)
        if art_science_filter_condition:
            student_queryset = student_queryset.filter(art_science__exact=art_science_filter_condition)
            filter_condition_list.append(art_science_filter_condition)
        if gender_filter_condition:
            student_queryset = student_queryset.filter(gender__exact=gender_filter_condition)
            filter_condition_list.append(gender_filter_condition)

        # 过滤器个数
        filter_count = len(filter_condition_list)
        # print(filter_condition_list, filter_count, score_queryset.count())

        # 搜索功能
        q_search_condition = request.GET.get('q')
        if q_search_condition:
            student_queryset = student_queryset.filter(
                Q(student_name__icontains=q_search_condition) |
                Q(teacher__name__icontains=q_search_condition)
                                                       )

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        if all_page_condition and student_queryset.count() > 0:
            # 每一页显示几条数据 如果all=1则显示全部
            page_count = student_queryset.count()
        else:
            page_count = 1
        p = Paginator(student_queryset, page_count, request=request)
        student_page = p.page(page)

        context = {
            'student_queryset': student_queryset,
            'grade_queryset': grade_queryset,
            'class_filter_queryset': class_filter_queryset,

            'grade_id': grade_filter_condition,  # 过滤器
            'art_science': art_science_filter_condition,
            'class_id': class_filter_condition,
            'gender': gender_filter_condition,
            'filter_count': filter_count,

            'q': q_search_condition,  # 搜索框

            'rel_clas__id': rel_class_condition,  # 外键筛选条件

            'clas': clas_select_condition,  # 排序条件
            'grade': grade_select_condition,
            'year_join': year_join_select_condition,

            'all': all_page_condition,
            'student_queryset_count': student_queryset.count(),  # 分页
            'student_page': student_page,

            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息'
        }
        return render(request, 'teacher/teacher_studentlist.html', context)


class TeacherStudentInfoView(LoginRequiredMixin, View):
    # 老师所教学生的详情页

    def get(self, request):

        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        student_file_number = request.GET.get('file_number')
        student = StudentInfo.objects.get(file_number__exact=int(student_file_number))

        context = {
            'student': student,
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息'
        }
        return render(request, 'teacher/teacher_studentinfo.html', context)


class TeacherScoreListView(LoginRequiredMixin, View):
    # 该班所有学生成绩列表

    def get(self, request):

        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        # 找出老师所教的班，只考虑老师当班主任或者当任课老师，不存在当班主任却教其他版的课
        if teacher.is_class_leader:
            class_queryset = teacher.classinfo_set.all().order_by('grade__year')
        else:
            class_queryset = ClassInfo.objects.filter(
                Q(chinese_teacher__number__exact=teacher.number) |
                Q(math_teacher__number__exact=teacher.number) |
                Q(english_teacher__number__exact=teacher.number) |
                Q(physical_teacher__number__exact=teacher.number) |
                Q(chemistry_teacher__number__exact=teacher.number) |
                Q(biology_teacher__number__exact=teacher.number) |
                Q(politics_teacher__number__exact=teacher.number) |
                Q(geography_teacher__number__exact=teacher.number) |
                Q(history_teacher__number__exact=teacher.number) |
                Q(sport_teacher__number__exact=teacher.number) |
                Q(music_teacher__number__exact=teacher.number)
            ).order_by('grade__year')

        # print(class_queryset, type(class_queryset))

        # 先查询出所有老师教的班 再查所有班的学生
        # 根据班级的id查询所有的学生
        class_id_list = [clas_.id for clas_ in class_queryset]
        student_queryset = StudentInfo.objects.filter(clas__id__in=class_id_list).all()
        # print(student_queryset, student_queryset.count())

        # 根据学生的档案号查询学生所有的成绩
        student_id_list = [student.file_number for student in student_queryset]
        score_queryset = ScoreInfo.objects.filter(file_number__file_number__in=student_id_list)

        # 关联查询
        rel_student_condition = request.GET.get('rel_student_number')
        if rel_student_condition and rel_student_condition is not None:
            score_queryset = score_queryset.filter(file_number__file_number__exact=int(rel_student_condition))

        # 从前端获取筛选条件并放入列表中
        chinese_select_condition = request.GET.get('chinese')
        math_select_condition = request.GET.get('math')
        english_select_condition = request.GET.get('english')
        physical_select_condition = request.GET.get('physical')
        chemistry_select_condition = request.GET.get('chemistry')
        biology_select_condition = request.GET.get('biology')
        politics_select_condition = request.GET.get('politics')
        geography_select_condition = request.GET.get('geography')
        history_select_condition = request.GET.get('history')
        sum_score_select_condition = request.GET.get('sum_score')
        grade_rank_select_condition = request.GET.get('grade_rank')
        class_rank_select_condition = request.GET.get('class_rank')

        all_page_condition = request.GET.get('all')  # 是否全部显示
        # print(chinese_select_condition)

        # 如果不为空,则放入同一个列表中
        select_condition_list = [chinese_select_condition, math_select_condition, english_select_condition,
                                 physical_select_condition, chemistry_select_condition, biology_select_condition,
                                 politics_select_condition, geography_select_condition, history_select_condition,
                                 sum_score_select_condition, grade_rank_select_condition, class_rank_select_condition, ]

        # 强制类型转换去除重复条件
        order_condition_list = [condition for condition in select_condition_list if condition]  # 去杂
        select_condition_set = set(order_condition_list)
        select_condition_list = list(select_condition_set)
        # print(select_condition_list)

        # 利用排序条件并通过外键关联查询老师当过班主任的班级
        try:
            select_condition_tuple = tuple(select_condition_list)  # 传入多个排序条件
            score_queryset = score_queryset.order_by(*select_condition_tuple)
        except Exception:
            score_queryset = score_queryset.all()

        # 过滤器
        exam_queryset = ExamList.objects.all().order_by('time')
        grade_queryset = GradeInfo.objects.all()
        filter_condition_list = []
        exam_filter_condition = request.GET.get('exam_id')
        grade_filter_condition = request.GET.get('grade_id')
        class_filter_condition = request.GET.get('class_id')

        # print(exam_filter_condition, grade_filter_condition, class_filter_condition, type(exam_filter_condition))

        # 过滤器筛选
        if exam_filter_condition and exam_filter_condition is not 'None':
            score_queryset = score_queryset.filter(which_exam__id__exact=int(exam_filter_condition))
            filter_condition_list.append(exam_filter_condition)
        if grade_filter_condition and grade_filter_condition is not 'None':
            score_queryset = score_queryset.filter(file_number__grade_id__exact=int(grade_filter_condition))
            filter_condition_list.append(grade_filter_condition)
        if class_filter_condition and class_filter_condition is not 'None':
            score_queryset = score_queryset.filter(file_number__clas_id__exact=int(class_filter_condition))
            filter_condition_list.append(class_filter_condition)

        # 过滤器个数
        filter_count = len(filter_condition_list)
        # print(filter_condition_list, filter_count, score_queryset.count())

        # 搜索功能
        q_search_condition = request.GET.get('q')
        if q_search_condition:
            score_queryset = score_queryset.filter(file_number__student_name__icontains=q_search_condition)

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        if all_page_condition and score_queryset.count() > 0:
            # 每一页显示几条数据 如果all=1则显示全部
            page_count = score_queryset.count()
        else:
            page_count = 1
        p = Paginator(score_queryset, page_count, request=request)
        score_page = p.page(page)

        # print(class_filter_condition)

        context = {
            'chinese': chinese_select_condition, # 排序条件
            'math': math_select_condition,
            'english': english_select_condition,
            'physical': physical_select_condition,
            'chemistry': chemistry_select_condition,
            'biology': biology_select_condition,
            'politics': politics_select_condition,
            'geography': geography_select_condition,
            'history': history_select_condition,
            'sum_score': sum_score_select_condition,
            'class_rank': class_rank_select_condition,
            'grade_rank': grade_rank_select_condition,

            'rel_student_number': rel_student_condition,  # 关联查询条件

            'q': q_search_condition,  # 搜索框

            'grade_id': grade_filter_condition, # 过滤器
            'class_id': class_filter_condition,
            'exam_id': exam_filter_condition,
            'filter_count': filter_count,

            'class_queryset': class_queryset, # queryset对象
            'grade_queryset': grade_queryset,
            'exam_queryset': exam_queryset,
            'score_queryset': score_queryset,

            'all': all_page_condition,
            'score_page': score_page,
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息'
        }

        return render(request, 'teacher/teacher_scorelist.html', context)


class TeacherScoreInfoView(LoginRequiredMixin, View):
    # 学生成绩详情页

    def get(self, request):

        # 确定老师身份
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        # 确定当前成绩和学生对象
        student_score_id = request.GET.get('score_id')
        if student_score_id:
            score = ScoreInfo.objects.get(score_id__exact=int(student_score_id))
            student = score.file_number
            context = {
                'teacher': teacher,
                'score': score,
                'student': student,
            }
            return render(request, 'teacher/teacher_scoreinfo.html', context)
        else:
            return redirect(reverse('teacher:teacher_scorelist'))

    def post(self, request):
        # 确定老师身份
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        # 确定当前成绩对象
        student_score_id = request.GET.get('score_id')
        score = ScoreInfo.objects.get(score_id__exact=int(student_score_id))

        chinese = request.POST.get('chinese')
        math = request.POST.get('math')
        english = request.POST.get('english')
        physical = request.POST.get('physical')
        chemistry = request.POST.get('chemistry')
        biology = request.POST.get('biology')
        politics = request.POST.get('politics')
        geography = request.POST.get('geography')
        history = request.POST.get('history')

        if teacher.is_class_leader:
            score.chinese, score.math, score.english, score.physical, score.chemistry, score.biology, score.politics, \
            score.geography, score.history = int(chinese), int(math), int(english), int(physical), int(chemistry), \
                                             int(biology), int(politics), int(geography), int(history)
            score.save()
        else:
            if teacher.subject == '语文' and chinese:
                score.chinese = int(chinese)
            elif teacher.subject == '数学' and math:
                score.math = int(math)
            elif teacher.subject == '英语' and english:
                score.english = int(english)
            elif teacher.subject == '物理' and physical:
                score.physical = int(physical)
            elif teacher.subject == '化学' and chemistry:
                score.chemistry = int(chemistry)
            elif teacher.subject == '生物' and biology:
                score.biology = int(biology)
            elif teacher.subject == '政治' and politics:
                score.politics = int(politics)
            elif teacher.subject == '历史' and history:
                score.history = int(history)
            elif teacher.subject == '地理' and geography:
                score.geography = int(geography)
            score.save()

        return redirect(reverse('teacher:teacher_scorelist'))