# Generated by Django 2.0.7 on 2018-10-07 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrator', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamList',
            fields=[
                ('id', models.IntegerField(db_column='考试序号', help_text='如：1，表示第一次考试', primary_key=True, serialize=False, verbose_name='考试序号')),
                ('time', models.CharField(db_column='考试时间', help_text='如：20180512表示2018年5月12日', max_length=8, verbose_name='考试时间')),
                ('remark', models.TextField(blank=True, db_column='备注', default='', max_length=100, null=True, verbose_name='备注')),
            ],
            options={
                'db_table': '考试次序表',
                'verbose_name_plural': '考试列表',
                'ordering': ['-time'],
                'verbose_name': '考试列表',
            },
        ),
        migrations.CreateModel(
            name='RewardPunishInfo',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_remark', models.TextField(blank=True, db_column='奖励详情', default='', help_text='该生所有奖励，每一条记录以逗号结尾', null=True, verbose_name='奖励详情')),
                ('punish_remark', models.TextField(blank=True, db_column='惩罚详情', default='', help_text='该生所有惩罚，每一条记录以逗号结尾', null=True, verbose_name='惩罚详情')),
            ],
            options={
                'db_table': '奖惩详情表',
                'verbose_name_plural': '奖惩管理',
                'verbose_name': '奖惩管理',
            },
        ),
        migrations.CreateModel(
            name='ScoreInfo',
            fields=[
                ('score_id', models.AutoField(db_column='成绩ID', primary_key=True, serialize=False, verbose_name='成绩ID')),
                ('exam_number', models.CharField(db_column='准考证号', default='xxxxxx', max_length=10, verbose_name='准考证号')),
                ('chinese', models.PositiveSmallIntegerField(db_column='语文', default=0, verbose_name='语文')),
                ('math', models.PositiveSmallIntegerField(db_column='数学', default=0, verbose_name='数学')),
                ('english', models.PositiveSmallIntegerField(db_column='英语', default=0, verbose_name='英语')),
                ('physical', models.PositiveSmallIntegerField(db_column='物理', default=0, verbose_name='物理')),
                ('chemistry', models.PositiveSmallIntegerField(db_column='化学', default=0, verbose_name='化学')),
                ('biology', models.PositiveSmallIntegerField(db_column='生物', default=0, verbose_name='生物')),
                ('politics', models.PositiveSmallIntegerField(db_column='政治', default=0, verbose_name='政治')),
                ('geography', models.PositiveSmallIntegerField(db_column='地理', default=0, verbose_name='地理')),
                ('history', models.PositiveSmallIntegerField(db_column='历史', default=0, verbose_name='历史')),
                ('remark', models.TextField(blank=True, db_column='备注', max_length=100, null=True, verbose_name='备注')),
                ('sum_score', models.PositiveSmallIntegerField(blank=True, db_column='总分', default=0, null=True, verbose_name='总分')),
                ('grade_rank', models.PositiveSmallIntegerField(db_column='年级排名', default=0, verbose_name='年级排名')),
                ('class_rank', models.PositiveSmallIntegerField(db_column='班级排名', default=0, verbose_name='班级排名')),
            ],
            options={
                'db_table': '具体成绩详情表',
                'verbose_name_plural': '成绩列表',
                'ordering': ['which_exam', 'file_number'],
                'verbose_name': '成绩列表',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('file_number', models.IntegerField(db_column='档案号', primary_key=True, serialize=False, verbose_name='档案号')),
                ('student_name', models.CharField(db_column='姓名', help_text='请输入您的真实姓名', max_length=5, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], db_column='性别', max_length=10, verbose_name='性别')),
                ('ID', models.CharField(db_column='身份证号', error_messages={'max_length': '身份证最多十八位', 'unique': '身份证号错误'}, help_text='请输入真实的身份证号', max_length=18, verbose_name='身份证号')),
                ('password', models.CharField(db_column='密码', default='xxxxxx', help_text='请输入密码', max_length=16, verbose_name='密码')),
                ('nation', models.CharField(db_column='民族', default='汉族', max_length=10, verbose_name='民族')),
                ('year_join', models.CharField(db_column='入学年份', help_text='请输入如：2018', max_length=4, verbose_name='入学年份')),
                ('bed_number', models.PositiveSmallIntegerField(db_column='床号', default=0, verbose_name='床号')),
                ('art_science', models.CharField(choices=[('art', '文科'), ('science', '理科'), ('all', '不分文理科')], db_column='文理科', default='all', max_length=7, verbose_name='文理科')),
                ('phone', models.CharField(db_column='联系电话', error_messages={'max_length': '手机号最多十一位'}, help_text='请输入正确的联系方式', max_length=11, verbose_name='电话')),
                ('address', models.TextField(blank=True, db_column='地址', default='', error_messages={'max_length': '最多不超过一百个字'}, help_text='最多不超过一百个字', max_length=100, null=True, verbose_name='地址')),
                ('remark', models.TextField(blank=True, db_column='备注', default='', max_length=100, null=True, verbose_name='备注')),
                ('clas', models.ForeignKey(db_column='班级', default='1', help_text='请保持您的入学年份上下相符', null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.ClassInfo', verbose_name='班级')),
                ('dormitory_number', models.ForeignKey(db_column='宿舍号', help_text='请保持您的入学年份上下相符', null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.DormitoryInfo', verbose_name='宿舍号')),
                ('grade', models.ForeignKey(db_column='年级', default='1', help_text='请保持您的入学年份上下相符', null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.GradeInfo', verbose_name='年级')),
                ('teacher', models.ForeignKey(blank=True, db_column='班主任编号', limit_choices_to={'is_class_leader': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teachers.TeacherInfo', verbose_name='班主任编号')),
            ],
            options={
                'db_table': '学生基本信息表',
                'verbose_name_plural': '学生信息表',
                'verbose_name': '学生信息表',
            },
        ),
        migrations.AddField(
            model_name='scoreinfo',
            name='file_number',
            field=models.ForeignKey(db_column='学生', null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.StudentInfo', verbose_name='学生'),
        ),
        migrations.AddField(
            model_name='scoreinfo',
            name='which_exam',
            field=models.ForeignKey(db_column='考试', null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.ExamList', verbose_name='考试'),
        ),
        migrations.AddField(
            model_name='rewardpunishinfo',
            name='student',
            field=models.ForeignKey(db_column='学生', null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.StudentInfo', verbose_name='学生'),
        ),
    ]
