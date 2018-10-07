from django.shortcuts import render, redirect, reverse
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from .models import TeacherInfo
from administrator.models import GradeInfo

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
        context = {
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
        print(get('remark'), teacher.remark)
        teacher.save()  # 保存到数据库

        return redirect(reverse('teacher:teacher_infoshow'))


class TeacherClassListView(LoginRequiredMixin, View):
    # 老师所教班级列表 先找出老师所教的班，然后在筛选

    def get(self, request):
        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)

        # 判断老师所教科目找出关联班级
        if teacher.subject in ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '地理', '历史', '体育', '音乐']:
            if teacher.subject == '语文':
                class_list = teacher.chinese_teacher_class.all()
            elif teacher.subject == '数学':
                class_list = teacher.math_teacher_class.all()
            elif teacher.subject == '英语':
                class_list = teacher.english_teacher_class.all()
            elif teacher.subject == '物理':
                class_list = teacher.physical_teacher_class.all()
            elif teacher.subject == '化学':
                class_list = teacher.chemistry_teacher_class.all()
            elif teacher.subject == '生物':
                class_list = teacher.biology_teacher_class.all()
            elif teacher.subject == '政治':
                class_list = teacher.politics_teacher_class.all()
            elif teacher.subject == '地理':
                class_list = teacher.geography_teacher_class.all()
            elif teacher.subject == '历史':
                class_list = teacher.history_teacher_class.all()
            elif teacher.subject == '体育':
                class_list = teacher.sport_teacher_class.all()
            else:
                class_list = teacher.music_teacher_class.all()
        else:
            # 无论是班主任，优先返回班主任管理班级，如果条件不符，返回一个空的queryset对象
            class_list = teacher.classinfo_set.all()

        # 从前端获取筛选条件并放入列表中
        o_select_condition = request.GET.get('o')
        p_select_condition = request.GET.get('p')

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
            class_list = class_list.order_by(*select_condition_tuple)
        except FieldError:
            class_list = class_list.all()

        # 过滤器
        grade_list = GradeInfo.objects.all().order_by('-year')
        grade_filter_condition = request.GET.get('grade')
        filter_condition_list = []
        if grade_filter_condition:
            class_list = class_list.filter(grade__id__exact=grade_filter_condition)
            filter_condition_list.append(grade_filter_condition)

        # 过滤器个数
        filter_count = len(filter_condition_list)

        # 搜索框
        search_condition = request.GET.get('_q_')
        if search_condition:
            class_list = class_list.filter(header__name__icontains=search_condition)

        # 获取筛选过的总数据量并传到前段
        class_list_count = len(class_list)

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        if request.GET.get('all') and  class_list_count > 0:
            # 每一页显示几条数据 如果all=1则显示全部
            page_count = class_list_count
        else:
            page_count = 5
        p = Paginator(class_list, page_count, request=request)
        class_list = p.page(page)

        context = {
            '_q_': search_condition,
            'grade_id': grade_filter_condition,
            'filter_count': filter_count,
            'grade_list': grade_list,
            'p': p_select_condition,
            'o': o_select_condition,
            'all': request.GET.get('all'),
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息',
            'class_list': class_list,
            'class_list_count': class_list_count
        }
        return render(request, 'teacher/teacher_classlist.html', context)


class TeacherStudentListView(LoginRequiredMixin, View):
    # 老师所教学生列表

    def get(self, request):

        # 通过session确定老师对象
        username = request.session.get('username')
        teacher = TeacherInfo.objects.get(number__exact=username)
        context = {
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
        context = {
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
        context = {
            'teacher': teacher,
            'teacher_name': teacher.name,
            'title': '基本信息'
        }

        return render(request, 'teacher/teacher_scorelist.html', context)


class TeacherScoreInfoView(LoginRequiredMixin, View):

    pass