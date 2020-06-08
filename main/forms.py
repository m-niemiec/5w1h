from django.forms import ModelForm
from .models import *
from django import forms


class AskAQuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Question
        fields = ['question']


class GiveAnAnswerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']
        widgets = {'question_id': forms.HiddenInput()}


# Form for selecting valued answer.
class BestAnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']
