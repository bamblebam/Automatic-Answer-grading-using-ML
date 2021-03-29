from django.urls import path
from . import views

urlpatterns = [
    path("new-question", views.newQuestionPage, name='new-question'),
    path("", views.QuestionListView.as_view(), name='index'),
    path('question/<slug>', views.questionPage, name='question'),
]
