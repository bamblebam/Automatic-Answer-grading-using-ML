from django.contrib import admin
from.models import Question, Response, Exam, ExamResponse
# Register your models here.
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Exam)
admin.site.register(ExamResponse)
