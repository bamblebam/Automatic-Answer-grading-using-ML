from .models import Question, Response
from django import forms


class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'model_answer']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'How to create a Q&A website with Django?'
            })
        }


class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
