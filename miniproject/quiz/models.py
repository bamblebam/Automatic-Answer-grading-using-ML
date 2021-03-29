from django.db import models
from user_auth.models import User
from django.template.defaultfilters import slugify
from uuid import uuid4
# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    model_answer = models.TextField(null=True)
    question_code = models.CharField(max_length=200, default=uuid4().hex[:6])
    slug = models.SlugField(max_length=255, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(Question, self).save(*args, **kwargs)


class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='responses')
    body = models.TextField(null=False)
    slug = models.SlugField(max_length=255, null=True)

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid4().hex[:10])
        super(Response, self).save(*args, **kwargs)
