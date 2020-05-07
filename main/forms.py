from django.forms import ModelForm
from .models import *
from django import forms


class AskAQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question']


class GiveAnAnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']
        widgets = {'question_id': forms.HiddenInput()}


class BestAnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']