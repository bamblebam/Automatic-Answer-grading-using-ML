from django.db import models
import django_filters
from django_filters import FilterSet
from .models import Question


class QuestionFilter(FilterSet):
    class Meta:
        model = Question
        fields = ['title', 'question_code']
