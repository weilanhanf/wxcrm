from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger

from .forms import LoginForm, RegisterForm
from .models import StudentInfo, ScoreInfo
from teachers.models import TeacherInfo
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class LoginView(View):
    """用户登录页"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        login_form = LoginForm(request.POST)  # form组件最前端数据进行校验
        if login_form.is_valid():
            # 如果表单验证成功，进行用户身份认证
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            character = request.POST.get("character")
            # print(username, password, character, type(username), type(password), type(character))
            try:
                if isinstance(username, str):
                    username = int(username)

                # 判断登录用户的身份，1为学生， 2为老师
                if character == "2":
                    user = TeacherInfo.objects.get(number=username, password=password)
                    red = HttpResponseRedirect(reverse('teacher:teacher_index'))  # 重定向到老师首页

                else:
                    user = StudentInfo.objects.get(file_number=username, password=password)
                    red = HttpResponseRedirect(reverse('student:student_index'))  # 重定向到学生首页

                if user is not None:
                    # 若当前用户可用，则设置cookie和session值做认证
                    red.set_cookie('username', username, max_age=-1)
                    request.session['username'] = username
                    request.session['is_login'] = True
                    request.session.set_expiry(0)
                    return red
                else:
                    # character 作为当老师认证登录失败的时候标识
                    return render(request, "login.html", {"msg": "用户名或者密码错误", 'character': character})
            except:
                return render(request, "login.html", {"msg": "用户名或者密码错误", 'character': character})
        else:
            return render(request, "login.html", {"msg": "用户名或者密码格式错误"})


class LogoutView(View):
    # 清除session
    def get(self, request):
        # 判断是否已经登录，在登录状态下清除session
        if not request.session.get('is_login', None):
            return redirect(reverse('login'))

        request.session.flush()
        return redirect(reverse('login'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 实例化form对象，进行验证
        register_form = RegisterForm(request.POST)  # request.post包含从前台发送的表单
        # print('生成form')
        if register_form.is_valid():
            username = request.POST.get('number', '')
            if StudentInfo.objects.filter(file_number=username):
                return render(request, "register.html", {"msg": "用户已经存在", "register_form": register_form})
            password = request.POST.get('password', '')
            # print(username, password)
            user_profile = StudentInfo()
            user_profile.file_number = username
            user_profile.password = password
            user_profile.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class StudentIndexView(LoginRequiredMixin, View):
    # 学生站点首页

    def get(self, request):
        username = request.session.get('username')
        student_name = StudentInfo.objects.get(file_number=username).student_name
        context = {
            'title': '首页',
            'student_name': student_name
        }
        return render(request, 'student/student_index.html', context=context)


class StudentInfoView(LoginRequiredMixin, View):
    # 学生基本信息页

    def get(self, request):
        username = request.session.get('username')
        student = StudentInfo.objects.get(file_number=username)
        context = {
            'title': '基本信息',
            'student': student
        }
        return render(request, 'student/student_info.html', context=context)


class StudentScoreView(LoginRequiredMixin, View):
    # 学生成绩列表页

    def get(self, request):
        username = request.session.get('username')
        student = StudentInfo.objects.get(file_number=username)
        student_name = student.student_name
        score_list = ScoreInfo.objects.filter(file_number__file_number=student.file_number).order_by('-which_exam')
        score_list_count = len(score_list)

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        if request.GET.get('all') and score_list_count > 0:
            # 每一页显示几条数据
            page_count = score_list_count
        else:
            page_count = 1
        p = Paginator(score_list, page_count, request=request)
        score_list = p.page(page)

        context = {
            'title': '成绩详情页',
            'score_list': score_list,
            'student_name': student_name,
            'score_list_count': score_list_count,
            'all': request.GET.get('all')
        }
        return render(request, 'student/student_score.html', context)
