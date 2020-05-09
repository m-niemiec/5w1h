from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question = models.CharField(max_length=300)
    answered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voteup = models.ManyToManyField(User, related_name='voteup', blank=True)
    votedown = models.ManyToManyField(User, related_name='votedown', blank=True)

    def __str__(self):
        return self.question

    def total_voteup(self):
        return self.voteup.count()

    def total_votedown(self):
        return self.votedown.count()


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, blank=False, null=True)
    answer = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appreciated_answer = models.BooleanField(default=False)

    class Meta:
        ordering = ['-appreciated_answer', '-id']

    def __str__(self):
        return self.answer

