# Generated by Django 2.0.7 on 2018-10-07 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='1', max_length=10, null=True, verbose_name='姓名')),
                ('month_score', models.PositiveSmallIntegerField(blank=True, db_column='月考分', default=0, null=True, verbose_name='月考分')),
                ('week_score', models.PositiveSmallIntegerField(blank=True, db_column='周考分', default=0, null=True, verbose_name='周考分')),
                ('grade_rank', models.PositiveSmallIntegerField(blank=True, db_column='年级排名', default=0, null=True, verbose_name='年级排名')),
                ('class_rank', models.PositiveSmallIntegerField(blank=True, db_column='班级排名', default=0, null=True, verbose_name='班级排名')),
            ],
            options={
                'db_table': '龙门详情表',
                'verbose_name_plural': '龙门',
                'verbose_name': '龙门',
            },
        ),
    ]
