from django.contrib import admin
from.models import Question, Response, Exam, ExamResponse
# Register your models here.
admin.site.register(Question)
admin.site.register(Response)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    filter_vertical = ('questions',)


@admin.register(ExamResponse)
class ExamResponseAdmin(admin.ModelAdmin):
    filter_vertical = ('responses',)
