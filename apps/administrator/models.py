from datetime import datetime, date

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

from teachers.models import TeacherInfo

# Create your models here.


class Administrator(AbstractUser):
    """管理人员"""

    id = models.AutoField(verbose_name='管理人员编号', db_column='管理员编号', primary_key=True)
    username = models.CharField(max_length=150, verbose_name='用户名', db_column='用户名', unique=True)
    password = models.CharField(max_length=128, verbose_name='密码', db_column='密码')
    email = models.EmailField(verbose_name='邮箱', db_column='邮箱', help_text='该邮箱将用来验证登录')
    add_time = models.DateTimeField(default=datetime.now, db_column='添加时间', verbose_name="添加时间")
    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注', default='',
                              help_text='备注不超过一百个汉字',
                              error_messages={
                                  'max_length': '备注不超过一百个字'
                              })

    class Meta:
        verbose_name = '管理人员'
        verbose_name_plural = verbose_name
        db_table = '管理人员表'

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """邮箱验证码"""

    SEND_CHOICES = (
        ("register", "注册"),
        ("forget", "找回密码"),
        ("update_email", "修改邮箱")
    )
    code = models.CharField(max_length=50, verbose_name="验证码", db_column='验证码')
    email = models.EmailField(max_length=50, verbose_name="邮箱", db_column='邮箱')
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name="发送类型", db_column='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间", db_column='发送时间')
    # 将now()中的括号去掉保证默认时间是models实例化的时间，而不是编译时间

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name
        db_table = '验证码表'

    def __str__(self):
        return self.code


class DormitoryInfo(models.Model):
    """宿舍信息"""

    dormitory_number = models.CharField(max_length=5, db_column='寝室号', verbose_name='寝室号', default='001')
    year = models.CharField(max_length=10, db_column='年份', default='2018', verbose_name='年份',)
    teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL,
                                null=True, verbose_name='老师档案号', db_column='老师档案号')
    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注',
                              help_text='备注不超过一百个汉字',
                              null=True, blank=True,
                              error_messages={
                                  'max_length': '备注不超过一百个字'
                              })

    class Meta:
        verbose_name = '宿舍'
        verbose_name_plural = verbose_name
        # ordering = ['year', 'dormitory_number']
        db_table = '宿舍信息表'
        unique_together = ['dormitory_number', 'year']

    def __str__(self):
        return "{0}年入住,宿舍号：{1}".format(self.year, self.dormitory_number)

    def get_dormitory_students(self):
        students_list = self.studentinfo_set.all()
        students_list = ','.join([i.student_name for i in students_list])
        return students_list
    get_dormitory_students.short_description = '宿舍学生'

    def get_student_number(self):
        num = self.studentinfo_set.all().count()
        return num
    get_student_number.short_description = '宿舍当前人数'


class GradeInfo(models.Model):
    """年级信息"""

    grade_number = models.CharField(max_length=2, db_column='年级', verbose_name='年级', default='1')
    year = models.CharField(max_length=10, db_column='届', verbose_name='届', default='2018', unique=True,
                            help_text='学生入学年份')
    header = models.CharField(max_length=10, db_column='年级主任', verbose_name='年级主任', default='', null=True, blank=True)
    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注',
                              default='', null=True, blank=True,
                              help_text='备注不超过一百个汉字',
                              error_messages={
                                  'max_length': '备注不超过一百个字'
                              })

    class Meta:
        verbose_name = '年级信息'
        verbose_name_plural = verbose_name
        db_table = '年级信息表'
        unique_together = ['grade_number', 'year']
        # ordering = ['-year', 'grade_number']  # datetime.time 对象不可序列化

    def __str__(self):

        year_now = date.today().year
        month_now = date.today().month

        #  计算出年级，但是为防止转校生，没有动态的加载到数据库
        if month_now >= 9 and year_now >= int(self.year):
            grade = year_now - int(self.year) + 1
        elif month_now < 9 and year_now >= int(self.year):
            grade = year_now - int(self.year)
        else:
            grade = int(self.grade_number)

        # 如果学生的年级大于三年级，则显示已经毕业
        if grade > 3:
            return '{0}届入学, 目前已毕业'.format(self.year)
        else:
            return '{0}届入学, 目前{1}年级'.format(self.year, grade)

    def save(self, *args, **kwargs):
        super(GradeInfo, self).save(*args, **kwargs)

    def get_class_number(self):
        # 通过关联查询该年级的所有班级数
        num = self.classinfo_set.count()
        return num
    get_class_number.short_description = '班级数'

    def get_grade_students_number(self):
        from students.models import StudentInfo
        num = StudentInfo.objects.filter(year_join=self.year).count()
        return num
    get_grade_students_number.short_description = '年级总人数'


class ClassInfo(models.Model):
    """班级信息"""

    class_number = models.CharField(max_length=5, db_column='班级', verbose_name='班级', default='1')
    header = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, null=True,
                               limit_choices_to={'is_class_leader': True},
                               verbose_name='班主任档案号', db_column='班主任档案号')
    grade = models.ForeignKey(GradeInfo, on_delete=models.SET_NULL, null=True, verbose_name='年级', db_column='年级')

    # 各科老师
    chinese_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='chinese_teacher_class',
                                        limit_choices_to={'subject': '语文'}, blank=True,
                                        null=True, verbose_name='语文老师', db_column='语文老师')
    math_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='math_teacher_class',
                                     limit_choices_to={'subject': '数学'}, blank=True,
                                     null=True, verbose_name='数学老师', db_column='数学老师')
    english_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='english_teacher_class',
                                        limit_choices_to={'subject': '英语'}, blank=True,
                                        null=True, verbose_name='英语老师', db_column='英语老师')
    physical_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='physical_teacher_class',
                                         limit_choices_to={'subject': '物理'}, blank=True,
                                         null=True, verbose_name='物理老师', db_column='物理老师')
    chemistry_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL,
                                          related_name='chemistry_teacher_class',
                                          limit_choices_to={'subject': '化学'}, blank=True,
                                          null=True, verbose_name='化学老师', db_column='化学老师')
    biology_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='biology_teacher_class',
                                        limit_choices_to={'subject': '生物'}, blank=True,
                                        null=True, verbose_name='生物老师', db_column='生物老师')
    politics_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='politics_teacher_class',
                                         limit_choices_to={'subject': '政治'}, blank=True,
                                         null=True, verbose_name='政治老师', db_column='政治老师')
    geography_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL,
                                          related_name='geography_teacher_class',
                                          limit_choices_to={'subject': '地理'}, blank=True,
                                          null=True, verbose_name='地理老师', db_column='地理老师')
    history_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='history_teacher_class',
                                        limit_choices_to={'subject': '历史'}, blank=True,
                                        null=True, verbose_name='历史老师', db_column='历史老师')
    sport_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='sport_teacher_class',
                                      limit_choices_to={'subject': '体育'}, blank=True,
                                      null=True, verbose_name='体育老师', db_column='体育老师')
    music_teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, related_name='music_teacher_class',
                                      limit_choices_to={'subject': '音乐'}, blank=True,
                                      null=True, verbose_name='音乐老师', db_column='音乐老师')

    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注',
                              default='', null=True, blank=True,
                              help_text='备注不超过一百个汉字',
                              error_messages={
                                  'max_length': '备注不超过一百个字'
                              })

    class Meta:
        verbose_name = '班级信息'
        verbose_name_plural = verbose_name
        # ordering = ['grade', 'class_number']
        db_table = '班级信息表'
        unique_together = ['grade', 'class_number', 'header']

    def __str__(self):
        return '班级：{}'.format(self.class_number)

    def get_class_student_number(self):
        # 根据班主任还有入学年份筛选
        num = self.studentinfo_set.all().count()
        return num
    get_class_student_number.short_description = '班级人数'

    def get_grade_leader(self):
        grade_leader = GradeInfo.objects.get(pk=self.grade.id).header
        return grade_leader
    get_grade_leader.short_description = '年级主任'
