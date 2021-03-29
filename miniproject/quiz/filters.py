from django.db import models
import django_filters
from django_filters import FilterSet
from .models import Question


class QuestionFilter(FilterSet):
    author = django_filters.CharFilter(
        field_name='author__username', label='Author', lookup_expr='icontains')

    class Meta:
        model = Question
        fields = {
            'title': ['icontains'],
            'question_code': ['exact']
        }
