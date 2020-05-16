from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


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


class BestAnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
