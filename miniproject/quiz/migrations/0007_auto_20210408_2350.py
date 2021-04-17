# Generated by Django 3.1.6 on 2021-04-08 18:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20210408_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='num_questions',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_code',
            field=models.CharField(blank=True, default='ec8f60', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_code',
            field=models.CharField(default='4ce524', max_length=200),
        ),
    ]
