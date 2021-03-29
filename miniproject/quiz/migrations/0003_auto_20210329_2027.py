# Generated by Django 3.1.6 on 2021-03-29 14:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210329_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='response',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='response',
            name='marks',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_code',
            field=models.CharField(default='9ac64e', max_length=200),
        ),
    ]
