from django.forms import ModelForm
from .models import *


class AskAQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question']


class GiveAnAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['question_id', 'answer']