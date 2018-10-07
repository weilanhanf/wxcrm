# Generated by Django 2.0.7 on 2018-10-07 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20181007_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='month_score',
            field=models.FloatField(blank=True, db_column='月考分', default=1, null=True, verbose_name='月考分'),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='week_score',
            field=models.FloatField(blank=True, db_column='周考分', default=1, null=True, verbose_name='周考分'),
        ),
    ]
