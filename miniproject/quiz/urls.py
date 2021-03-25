from django.urls import path
from . import views

urlpatterns = [
    path("new-question", views.newQuestionPage, name='new-question'),
    path("index/", views.homePage, name='index'),
    path('question/<int:id>', views.questionPage, name='question'),
]
