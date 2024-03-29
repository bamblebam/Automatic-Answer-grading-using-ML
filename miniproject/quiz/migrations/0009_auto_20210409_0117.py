# Generated by Django 3.1.6 on 2021-04-08 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0008_auto_20210409_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_code',
            field=models.CharField(blank=True, default='55b8bf', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_code',
            field=models.CharField(default='9dd78c', max_length=200),
        ),
        migrations.AlterField(
            model_name='response',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
