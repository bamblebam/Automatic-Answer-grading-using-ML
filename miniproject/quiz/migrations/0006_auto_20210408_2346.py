# Generated by Django 3.1.6 on 2021-04-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210408_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_code',
            field=models.CharField(blank=True, default='774871', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_code',
            field=models.CharField(default='e617a5', max_length=200),
        ),
    ]
