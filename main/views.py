from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django import forms
from django.template.loader import render_to_string
from main.models import Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    # Getting all needed query to render questions.
    allquestionswithanswers = Question.objects.filter(datecompleted__isnull=False).order_by('-id')
    allquestionswithoutanswers = Question.objects.filter(datecompleted__isnull=True).order_by('-id')
    allquestions = Question.objects.all().order_by('-id')

    # Counting for home page statistics.
    questions_count = Question.objects.count
    answers_count = Answer.objects.count

    # Code for pagination
    paginator = Paginator(allquestions, 2)
    page = request.GET.get('page')
    try:
        allquestions = paginator.page(page)
    except PageNotAnInteger:
        allquestions = paginator.page(1)
    except EmptyPage:
        allquestions = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(allquestions, index=4)

    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'allquestionswithanswers': allquestionswithanswers,
        'allquestionswithoutanswers': allquestionswithoutanswers,
        'questions_count': questions_count,
        'answers_count': answers_count,
        'allquestions': allquestions,
        'page_range': page_range
    }

    return render(request, 'main/home.html', context)


def proper_pagination(allquestions, index):
    start_index = 0
    end_index = 7
    if allquestions.number > index:
        start_index = allquestions.number - index
        end_index = start_index + end_index
    return start_index, end_index


def signupuser(request):
    if request.method == "GET":
        return render(request, 'main/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # Create a new user
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                messages.success(request, "Thank you for registering, have fun!")
                return redirect("dashboard")
            except IntegrityError:
                return render(request, 'main/signupuser.html', {'form': UserCreationForm(),
                                                                'error': "That user name is already taken. Please "
                                                                         "choose a different, new one."})

        else:
            return render(request, 'main/signupuser.html', {'form': UserCreationForm(),
                                                            'error': "Passwords did not match."})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'main/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': "Username and password did not match."})
        else:
            login(request, user)
            messages.success(request, "Thank you for logging in, have fun!")
            return redirect("dashboard")


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You logged out!")
        return redirect("home")


# Dashboard is mainpage for user, listing all his questions and answers. User gets redirected here after login.
@login_required
def dashboard(request):
    yourquestions = Question.objects.filter(user=request.user)
    youranswers = Answer.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html', {'yourquestions': yourquestions, 'youranswers': youranswers})


@login_required
def askaquestion(request):
    if request.method == 'GET':
        return render(request, 'main/askaquestion.html', {'form': AskAQuestionForm()})
    else:
        try:
            form = AskAQuestionForm(request.POST)
            new_question = form.save(commit=False)
            new_question.user = request.user
            new_question.save()
            messages.success(request, "You asked a question! Thank You.")
            return redirect("dashboard")
        except ValueError:
            return render(request, 'main/askaquestion.html',
                          {'form': AskAQuestionForm(), 'error': 'Bad input, can you please rephrase?'})


# Allows user to edit his question.
@login_required
def viewquestion(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk, user=request.user)
    if request.method == "GET":
        form = AskAQuestionForm(instance=question)
        return render(request, 'main/viewquestion.html', {'question': question,
                                                          'form': form})
    else:
        try:
            form = AskAQuestionForm(request.POST, instance=question)
            form.save()
            return redirect('dashboard')
        except ValueError:
            return render(request, 'main/viewquestion.html', {'question': question,
                                                              'form': form,
                                                              'error': 'Bad input, can you please rephrase?'})


# Question details show when user click on question from main page.
def questiondetails(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    appreciated_answer = Answer.objects.filter(question_id=question).values('appreciated_answer').exists()
    question_form_id = question
    total_voteup = question.total_voteup()
    total_votedown = question.total_votedown()
    is_voteup = False
    is_votedown = False
    form = GiveAnAnswerForm(request.POST, initial={'question_id': 'question_form_id'})
    if request.method == 'POST':
        new_answer = form.save(commit=False)
        new_answer.user = request.user
        new_answer.save()
        messages.success(request, "You answered question! Thank You.")
    if question.voteup.filter(id=request.user.id).exists():
        is_voteup = True
    if question.votedown.filter(id=request.user.id).exists():
        is_votedown = True

    context = {
        'form': GiveAnAnswerForm(initial={'question_id': question_form_id}),
        'BestAnswer_form': BestAnswerForm(initial={'question_id': question_form_id}),
        'question': question,
        'is_voteup': is_voteup,
        'is_votedown': is_votedown,
        'total_voteup': total_voteup,
        'total_votedown': total_votedown,
        'appreciated_answer': appreciated_answer
    }

    return render(request, 'main/questiondetails.html', context)


@login_required
def deletequestion(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk, user=request.user)
    if request.method == "POST":
        question.delete()
        messages.success(request, "Question deleted!")
        return redirect("dashboard")


# Marks question as "Answered".
@login_required
def questionanswered(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk, user=request.user)
    if request.method == "POST":
        question.datecompleted = timezone.now()
        question.answered = True
        question.save()
        messages.success(request, "You marked your question as answered!")
        return redirect("dashboard")


# Allows user to edit his answer.
@login_required
def viewanswer(request, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk, user=request.user)
    if request.method == "GET":
        form = GiveAnAnswerForm(instance=answer)
        return render(request, 'main/viewanswer.html', {'answer': answer, 'form': form})
    else:
        try:
            form = GiveAnAnswerForm(request.POST, instance=answer)
            form.save()
            return redirect('dashboard')
        except ValueError:
            return render(request, 'main/viewanswer.html', {'answer': answer, 'form': form,
                                                            'error': 'Bad input, can you please rephrase?'})


@login_required
def deleteanswer(request, answer_pk):
    answer = get_object_or_404(Question, pk=answer_pk, user=request.user)
    if request.method == "POST":
        answer.delete()
        messages.success(request, "Answer deleted!")
        return redirect("dashboard")


# Voting system, when you select UP or DOWN other button will disappear. Uses Ajax.
@login_required
def voteup(request):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    is_voteup = False
    if question.voteup.filter(id=request.user.id).exists():
        question.voteup.remove(request.user)
        is_voteup = False
        total_voteup = question.total_voteup()
        total_votedown = question.total_votedown()
    else:
        question.voteup.add(request.user)
        is_voteup = True
        total_voteup = question.total_voteup()
        total_votedown = question.total_votedown()
    context = {
        'question': question,
        'is_voteup': is_voteup,
        'total_voteup': total_voteup,
        'total_votedown': total_votedown
    }
    if request.is_ajax():
        html = render_to_string('main/partials/voting_section.html', context, request=request)
        return JsonResponse({'form': html})


@login_required
def votedown(request):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    is_votedown = False
    if question.votedown.filter(id=request.user.id).exists():
        question.votedown.remove(request.user)
        is_votedown = False
        total_voteup = question.total_voteup()
        total_votedown = question.total_votedown()
    else:
        question.votedown.add(request.user)
        is_votedown = True
        total_voteup = question.total_voteup()
        total_votedown = question.total_votedown()
    context = {
        'question': question,
        'is_votedown': is_votedown,
        'total_voteup': total_voteup,
        'total_votedown': total_votedown
    }
    if request.is_ajax():
        html = render_to_string('main/partials/voting_section.html', context, request=request)
        return JsonResponse({'form': html})


# System for marking which answer was actually valuable for user who asked the question.
@login_required
def appreciatedanswer(request, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk)
    if request.method == "POST":
        answer.appreciated_answer = True
        answer.save()
        messages.success(request, "Answer marked as valued!")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


# About page that can be accessed from menu.
def about(request):
    return render(request, 'main/about.html')
