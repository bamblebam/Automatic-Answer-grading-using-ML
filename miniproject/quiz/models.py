from django.db import models
# from django.contrib.auth.models import User
from user_auth.models import User
# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    model_answer = models.TextField(null=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, null=False, on_delete=models.CASCADE, related_name='responses')
    body = models.TextField(null=False)
 
    def __str__(self):
        return self.body


