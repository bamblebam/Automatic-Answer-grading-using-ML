# Generated by Django 3.1.6 on 2021-04-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20210408_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_code',
            field=models.CharField(blank=True, default='cb965e', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_code',
            field=models.CharField(default='bc4ad2', max_length=200),
        ),
    ]