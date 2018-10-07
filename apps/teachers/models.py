from django.db import models

# Create your models here.


class TeacherInfo(models.Model):
    """教师基本信息表"""

    number = models.IntegerField(verbose_name='教师序号', db_column='教师序号', primary_key=True)
    name = models.CharField(max_length=5, verbose_name='姓名', db_column='姓名', default='male')
    gender = models.CharField(max_length=10, verbose_name='性别', db_column='性别', default='男', null=True, blank=True)
    password = models.CharField(max_length=16, verbose_name='密码', db_column='密码',
                                default='xxxxxx',
                                error_messages={
                                    'max_length': '不超过十六位'
                                })
    is_class_leader = models.BooleanField(default=False, verbose_name='是否为班主任', db_column='是否为班主任')
    email = models.EmailField(verbose_name='邮箱', db_column='邮箱', help_text='该邮箱将用来验证登录')
    phone = models.CharField(max_length=11, verbose_name='电话', db_column='联系电话', help_text='请输入正确的联系方式',
                             error_messages={
                                 'max_length': '手机号最多十一位'
                             })
    ID = models.CharField(max_length=18, verbose_name='身份证号', db_column='身份证号',
                          help_text='请输入真实的身份证号',
                          error_messages={
                              'unique': '身份证号错误',
                              'max_length': '身份证最多十八位',
                          })
    subject = models.CharField(max_length=25, verbose_name='教授科目', db_column='教授科目',
                               help_text='您教授的科目，如：语文',
                               default='', null=True, blank=True)
    remark = models.TextField(max_length=100, verbose_name='备注', db_column='备注',
                              default='', null=True, blank=True,
                              help_text='备注不超过一百个汉字',
                              error_messages={
                                  'max_length': '备注不超过一百个字'
                              })

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
        db_table = '教师信息表'

    def save(self, *args, **kwargs):
        # 重写父类的save方法，并添加功能

        # 将登陆密码改为身份证后六位
        if self.password == 'xxxxxx':
            self.password = self.ID[-6:]
        super(TeacherInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_student_number(self):
        num = self.studentinfo_set.all().count()
        return num
    get_student_number.short_description = '老师所教学生数'

