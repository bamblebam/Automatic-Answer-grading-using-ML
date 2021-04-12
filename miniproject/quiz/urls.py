from django.urls import path
from . import views

urlpatterns = [
    path("new-question", views.newQuestionPage, name='new-question'),
    path("", views.QuestionListView.as_view(), name='quiz-home'),
    path("exams/", views.ExamListView.as_view(), name='exam-home'),
    path('question/<slug>', views.questionPage, name='question'),
    path('responses/<slug>', views.QuestionResponseView.as_view(), name='responses'),
    path('response-update/<slug>',
         views.ResponseUpdateView.as_view(), name='response-update'),
    path('new-exam',
         views.CreateExam.as_view(), name='new-exam'),
    path('new-exam-response/<slug>',
         views.CreateExamResponse.as_view(), name='new-exam-response'),
    path('exam-responses/<slug>',
         views.ExamResponseView.as_view(), name='exam-responses'),
    path('add-questions/<slug>', views.addQuestionsToExam, name='add-questions'),
    path('add-response/<slug>', views.addResponseToExam, name='add-response'),
    path('errors/already-answered', views.already_answered, name='already-answered')
]
