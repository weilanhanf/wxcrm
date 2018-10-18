from __future__ import unicode_literals
# from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from teachers.models import TeacherInfo
from administrator.models import DormitoryInfo, ClassInfo, GradeInfo

# Create your models here.


class StudentInfo(models.Model):
    """学生基本信息表"""

    GENDER_CHOICE = (("male", "男"), ("female", "女"))
    ART_SCIENCE_CHOICES = (('art', '文科'), ('science', '理科'), ('all', '不分文理科'))

    file_number = models.IntegerField(primary_key=True, verbose_name='档案号', db_column='档案号')
    student_name = models.CharField(max_length=5, verbose_name="姓名", db_column='姓名', help_text='请输入您的真实姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, verbose_name='性别', db_column='性别')
    ID = models.CharField(max_length=18,
                          verbose_name='身份证号',
                          db_column='身份证号',
                          help_text='请输入真实的身份证号',
                          error_messages={
                               'unique': '身份证号错误',
                               'max_length': '身份证最多十八位',
                          })
    password = models.CharField(max_length=16, verbose_name='密码', db_column='密码', help_text='请输入密码', default='xxxxxx')
    nation = models.CharField(max_length=10, verbose_name='民族', db_column='民族', default='汉族')
    teacher = models.ForeignKey(TeacherInfo, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'is_class_leader': True},
                                verbose_name='班主任编号', db_column='班主任编号')  # 外键 筛选是班主任的老师
    year_join = models.CharField(max_length=4, verbose_name='入学年份', db_column='入学年份', help_text='请输入如：2018')
    grade = models.ForeignKey(GradeInfo, verbose_name='年级', on_delete=models.SET_NULL,
                              help_text='请保持您的入学年份上下相符',
                              null=True, db_column='年级', default='1')  # 外键
    clas = models.ForeignKey(ClassInfo, verbose_name='班级', on_delete=models.SET_NULL,
                             help_text='请保持您的入学年份上下相符',
                             null=True, db_column='班级', default='1')  # 外键
    dormitory_number = models.ForeignKey(DormitoryInfo, on_delete=models.SET_NULL, null=True,
                                         help_text='请保持您的入学年份上下相符',
                                         verbose_name='宿舍号', db_column='宿舍号')  # 外键
    bed_number = models.PositiveSmallIntegerField(verbose_name='床号', db_column='床号', default=0)
    art_science = models.CharField(max_length=7,
                                   verbose_name='文理科',
                                   db_column='文理科',
                                   choices=ART_SCIENCE_CHOICES,
                                   default='all')
    phone = models.CharField(max_length=11, verbose_name='电话', db_column='联系电话', help_text='请输入正确的联系方式',
                             error_messages={
                                 'max_length': '手机号最多十一位'
                             })
    address = models.TextField(max_length=100, verbose_name='地址', db_column='地址', default='', null=True, blank=True,
                               help_text='最多不超过一百个字',
                               error_messages={
                                   'max_length': '最多不超过一百个字',
                               })
    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注', default='', null=True, blank=True)

    class Meta:
        verbose_name = '学生信息表'
        verbose_name_plural = verbose_name
        db_table = '学生基本信息表'

    def save(self, *args, **kwargs):
        # 重写父类的save方法，并添加功能

        # 将学生登陆密码改为身份证后六位
        if self.password == 'xxxxxx':
            self.password = self.ID[-6:].lower()
        super(StudentInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.student_name

    def get_grade_class(self):
        return '{0}年级{1}'.format(self.gender, self.clas)
    get_grade_class.short_description = '班级年级'

    def get_all_score(self):
        return self.scoreinfo_set.all()
    get_all_score.short_description = '所有成绩'


class ExamList(models.Model):
    """考试列表"""

    id = models.IntegerField(verbose_name='考试序号', db_column='考试序号', help_text='如：1，表示第一次考试', primary_key=True)
    time = models.CharField(max_length=8, verbose_name='考试时间', db_column='考试时间',
                            help_text='如：20180512表示2018年5月12日', unique=True)
    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注', default='', null=True, blank=True)

    class Meta:
        verbose_name = '考试列表'
        verbose_name_plural = verbose_name
        db_table = '考试次序表'
        # unique_together = ['time']
        # ordering = ['-time']

    def __str__(self):
        time = self.time
        return '第{0}次考试，时间为{1}年{2}月{3}日'.format(self.id, time[:4], time[4:6], time[6:])

    def get_all_score(self):
        # 此次考试所有学生成绩
        return self.scoreinfo_set.all()
    get_all_score.short_description = '所有成绩'


class ScoreInfo(models.Model):
    """学生成绩详情表"""

    score_id = models.AutoField(verbose_name='成绩ID', db_column='成绩ID', primary_key=True)
    file_number = models.ForeignKey(StudentInfo, on_delete=models.SET_NULL, null=True,
                                    verbose_name='学生', db_column='学生')
    exam_number = models.CharField(max_length=10, verbose_name='准考证号', db_column='准考证号', default='xxxxxx')
    which_exam = models.ForeignKey(ExamList, on_delete=models.SET_NULL, null=True, verbose_name='考试', db_column='考试')

    # 各项成绩
    chinese = models.PositiveSmallIntegerField(verbose_name='语文', db_column='语文', default=0)
    math = models.PositiveSmallIntegerField(verbose_name='数学', db_column='数学', default=0)
    english = models.PositiveSmallIntegerField(verbose_name='英语', db_column='英语', default=0)
    physical = models.PositiveSmallIntegerField(verbose_name='物理', db_column='物理', default=0)
    chemistry = models.PositiveSmallIntegerField(verbose_name='化学', db_column='化学', default=0)
    biology = models.PositiveSmallIntegerField(verbose_name='生物', db_column='生物', default=0)
    politics = models.PositiveSmallIntegerField(verbose_name='政治', db_column='政治', default=0)
    geography = models.PositiveSmallIntegerField(verbose_name='地理', db_column='地理', default=0)
    history = models.PositiveSmallIntegerField(verbose_name='历史', db_column='历史', default=0)

    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注', blank=True, null=True)

    sum_score = models.PositiveSmallIntegerField(verbose_name='总分', db_column='总分', null=True, blank=True, default=0)
    grade_rank = models.PositiveSmallIntegerField(verbose_name='年级排名', db_column='年级排名', default=0)
    class_rank = models.PositiveSmallIntegerField(verbose_name='班级排名', db_column='班级排名', default=0)

    class Meta:
        verbose_name = '成绩列表'
        verbose_name_plural = verbose_name
        db_table = '具体成绩详情表'
        # unique_together = ['file_number', 'which_exam']
        # ordering = ['-which_exam', '-sum_score']

    def save(self, *args, **kwargs):
        # 覆盖save方法并增加功能

        # save方法中需要用到的变量
        exam_id = self.which_exam.id  # 确定本次考试的ID
        grade = self.file_number.grade  # 确定本次考试的年级
        clas = self.file_number.clas  # 确定年级

        # 如果当前成绩仍未默认值则更新总分字段
        # if self.sum_score == 0:
        subject = [self.chinese, self.math, self.english, self.physical, self.chemistry,
                   self.biology, self.politics, self.geography, self.history]
        total = sum(subject)

        # 如果排名仍为0则更新年级排名
        if self.grade_rank == 0:
            self.sum_score = total
            all_scores_grade_list = list(ScoreInfo.objects.filter(
                which_exam__id=exam_id,
                file_number__grade__id=grade.id
            ).order_by('sum_score'))  # 将本次考试的所有成绩记录排序并列表化
            ordered_scores_grade_list = [i.sum_score for i in all_scores_grade_list]  # 获取所有的成绩

            from bisect import bisect_right, bisect_left  # 二分法
            # 用法
            # >>> bisect.bisect_right([1, 3, 3, 4], 3)
            # 3
            # >>> bisect.bisect_left([1, 3, 3, 4], 3)
            # 1
            insert_grade_position = bisect_right(ordered_scores_grade_list, self.sum_score)
            grade_rank = len(ordered_scores_grade_list) - insert_grade_position + 1
            self.grade_rank = grade_rank  # 更新当前成绩排名

            # 在更新排名之后，要将比分数小的记录排名加一
            need_score_grade_int = bisect_left(ordered_scores_grade_list, self.sum_score)  # 从need_score_int之后的成绩记录排名都需要加一
            need_scores_grade_list = all_scores_grade_list[:need_score_grade_int]  # 比当前成绩总分和大的成绩记录
            for score in need_scores_grade_list:
                score.grade_rank += 1  # 每一项记录的排名加一
                score.save()  # 保存修改
        else:
            if self.sum_score != total:
                # 数据库中总分与计算后的综合不相等，则说明是修改状态
                score_grade_queryset = ScoreInfo.objects.filter(
                    which_exam__id=exam_id,
                    file_number__grade__id=grade.id
                ).order_by('-sum_score')

                # 找出比total大的总分排序
                score_gt_grade_queryset = score_grade_queryset.filter(sum_score__gt=total)
                if self in score_gt_grade_queryset:
                    # 如果self在比当前总分大的查询set中，说明分数是降低的,去除本身
                    score_gt_grade_queryset = score_gt_grade_queryset.exclude(score_id__exact=self.score_id)

                if score_gt_grade_queryset.exists():
                    # 按照比自己分数大的记录数，排名+1
                    self.grade_rank = score_gt_grade_queryset.count() + 1
                else:
                    # 如果不存在总分比total大的成绩，则自己排名第一
                    self.grade_rank = 1

                if self.sum_score < total:
                    # 分数升高，则要将比自己原来分数高但又比total低的成绩排名降低，排名+1
                    for score in score_grade_queryset:
                        if self.sum_score <= score.sum_score < total:
                            score.grade_rank += 1
                            score.save()
                else:
                    for score in score_grade_queryset:
                        # 分数降低，则要将比自己原来分数低但又比total高的成绩排名提高，排名-1
                        if self.sum_score > score.sum_score >= total:
                            score.grade_rank -= 1
                            score.save()

                # 到最后再讲total保存到数据库中
                self.sum_score = total

        # 如果排名仍为0则更新年级排名
        if self.class_rank == 0:
            self.sum_score = total
            all_scores_class_list = list(ScoreInfo.objects.filter(
                which_exam__id__exact=exam_id,
                file_number__grade__id__exact=grade.id,
                file_number__clas_id__exact=clas.id
            ).order_by('sum_score'))  # 将本次考试的所有成绩记录排序并列表化
            ordered_scores_class_list = [i.sum_score for i in all_scores_class_list]  # 获取所有的成绩

            from bisect import bisect_right, bisect_left  # 二分法
            # 用法
            # >>> bisect.bisect_right([1, 3, 3, 4], 3)
            # 3
            # >>> bisect.bisect_left([1, 3, 3, 4], 3)
            # 1
            insert_class_position = bisect_right(ordered_scores_class_list, self.sum_score)
            class_rank = len(ordered_scores_class_list) - insert_class_position + 1
            self.class_rank = class_rank  # 更新当前成绩排名

            # 在更新排名之后，要将比分数小的记录排名加一
            need_score_class_int = bisect_left(ordered_scores_class_list, self.sum_score)  # 从need_score_int之后的成绩记录排名都需要加一
            need_scores_class_list = all_scores_class_list[:need_score_class_int]  # 比当前成绩总分和大的成绩记录
            for score in need_scores_class_list:
                score.class_rank += 1  # 每一项记录的排名加一
                score.save()  # 保存修改
        else:
            if self.sum_score != total:
                # 数据库中总分与计算后的综合不相等，则说明是修改状态
                score_class_queryset = ScoreInfo.objects.filter(
                    which_exam__id__exact=exam_id,
                    file_number__grade__id__exact=grade.id,
                    file_number__clas_id__exact=clas.id
                ).order_by('-sum_score')

                # 找出比total大的总分排序
                score_gt_class_queryset = score_class_queryset.filter(sum_score__gt=total)
                if self in score_gt_class_queryset:
                    # 如果self在比当前总分大的查询set中，说明分数是降低的,去除本身
                    score_gt_class_queryset = score_gt_class_queryset.exclude(score_id__exact=self.score_id)

                if score_gt_class_queryset.exists():
                    # 按照比自己分数大的记录数，排名+1
                    self.class_rank = score_gt_class_queryset.count() + 1
                else:
                    # 如果不存在总分比total大的成绩，则自己排名第一
                    self.class_rank = 1

                if self.sum_score < total:
                    # 分数升高，则要将比自己原来分数高但又比total低的成绩排名降低，排名+1
                    for score in score_class_queryset:
                        if self.sum_score <= score.sum_score < total:
                            score.class_rank += 1
                            score.save()
                else:
                    for score in score_class_queryset:
                        # 分数降低，则要将比自己原来分数低但又比total高的成绩排名提高，排名-1
                        if self.sum_score > score.sum_score >= total:
                            score.class_rank -= 1
                            score.save()

                # 到最后再讲total保存到数据库中
                self.sum_score = total

        super(ScoreInfo, self).save(*args, **kwargs)

    # https://stackoverflow.com/questions/1471909/django-model-delete-not-triggered?noredirect=1&lq=1
    # 重写覆盖delete方法失效，原因是这里以管理员身份删除多条记录不会再直接调用delete方法 业务逻辑写在adminx中
    # def delete(self, *args, **kwargs):
    #     super(ScoreInfo, self).delete(*args, **kwargs)

    def __str__(self):
        time = self.which_exam.time
        return '{0}在{1}年{2}月{3}的考试'.format(self.file_number.student_name, time[:4], time[4:6], time[6:])

    def get_student_class(self):
        class_ = self.file_number.clas
        return class_
    get_student_class.short_description = '班级'

    def get_student_grade(self):
        grade = self.file_number.grade
        return grade
    get_student_grade.short_description = '年级'


class RewardPunishInfo(models.Model):
    """奖惩详情表"""

    id = models.AutoField(primary_key=True, db_column='ID', verbose_name='ID')
    student = models.ForeignKey(StudentInfo, on_delete=models.SET_NULL, null=True, db_column='学生', verbose_name='学生')
    reward_remark = models.TextField(verbose_name='奖励详情', db_column='奖励详情', default='', null=True, blank=True,
                                     help_text='该生所有奖励，每一条记录以逗号结尾')
    punish_remark = models.TextField(verbose_name='惩罚详情', db_column='惩罚详情', default='', null=True, blank=True,
                                     help_text='该生所有惩罚，每一条记录以逗号结尾')

    class Meta:
        verbose_name = '奖惩管理'
        verbose_name_plural = verbose_name
        db_table = '奖惩详情表'
        unique_together = ['student']

    def __str__(self):
        return '{}同学的奖惩措施'.format(self.student)

    def get_reward_sum(self):
        # 将奖励详情的字符串切成列表，并计算有多少条奖励记录
        reward_list = [i for i in self.reward_remark.replace('，', ',').split(',') if i is not '']
        return len(reward_list)
    get_reward_sum.short_description = '奖励总数'

    def get_punish_remark(self):
        # 将惩罚详情的字符串切成列表，并计算有多少条惩罚记录
        punish_list = [i for i in self.punish_remark.replace('，', ',').split(',') if i is not '']
        return len(punish_list)
    get_punish_remark.short_description = '惩罚总数'
