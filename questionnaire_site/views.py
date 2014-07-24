__author__ = 'alina'

from models import Likert_Scale_Answer, Text_Answer, Boolean_Answer, Participant, Question, Survey


from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from questionnaire_site.forms import SurveyForm, QuestionForm, ParticipantForm, \
    Likert_Scale_Answer_Form, Text_Answer_Form, Boolean_Answer_Form\
    # , UserForm

def index(request):
    return render_to_response('index.html')

def viewAnswers(request):

    survey_id = request.GET.get('survey', '')
    email_id = request.GET.get('email', '')

    survey = Survey.objects.get(title=survey_id)

    participant = Participant.objects.get(email=email_id)
    questions = Question.objects.filter(survey=survey)

    list = []

    likert_results = Likert_Scale_Answer.objects.filter(user=participant, question=questions)
    text_results = Text_Answer.objects.filter(user=participant, question=questions)
    boolean_results = Boolean_Answer.objects.filter(user=participant, question=questions)

    for answer in likert_results:
        list.append("<p>"  + str(answer.question.question_description) + " " + str(answer.choice) + "</p>")

    for answer in text_results:
        list.append("<p>"  + str(answer.question.question_description) + " " + str(answer.text) + "</p>")

    for answer in boolean_results:
        list.append("<p>"  + str(answer.question.question_description) + " " + str(answer.text) + "</p>")


    context_dict = {'likert_results': likert_results,
                    'text_results': text_results,
                    'boolean_results': boolean_results,
                    'survey': survey,
                    'participant': participant}

    # http://127.0.0.1:8000/view_answers/?survey=Survey4&email=participant4@gmail.com
    # Population script: participant X & survey X with answers in the x0-x9 range (participant9, survey9, answers 90-99)

    return render_to_response('survey.html',
                              context_dict, )

def viewSurvey(request):
    survey_id = request.GET.get('survey', '') # based on survey title
    survey = Survey.objects.get(title=survey_id)
    questions = Question.objects.filter(survey=survey)
    context = RequestContext(request)
    form = QuestionForm()
    context_dict = {'questions': questions,
                    'survey': survey,
                    'form': form}
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse ("done")
        else:
            print form.errors
    return render_to_response('survey.html',
                              context_dict,
                              context)

def add_survey(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # user = form.cleaned_data['user']
            # title = form.cleaned_data['title']
            # description = form.cleaned_data['description']
            # deadline = form.cleaned_data['deadline']
            # Survey.objects.create(user=user, title=title, description=description, deadline=deadline)
            form.save(commit = True)
            return HttpResponseRedirect('/view_survey/?survey=' + form.cleaned_data['title'])
        else:
            print form.errors
    else:
        form = SurveyForm()
    return render_to_response('add_survey.html', {'form': form}, context)


def add_question(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            # return render_to_response('index.html')
            return HttpResponse("Created Question")
        else:
            print form.errors
    else:
        form = QuestionForm()
    return render_to_response('add_question.html', {'form': form}, context)


def add_participant(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return render_to_response('index.html')
            # return HttpResponse("Participant Added")
        else:
            print form.errors
    else:
        form = ParticipantForm()
    return render_to_response('add_participant.html', {'form': form}, context)


def add_likert_scale_answer(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = Likert_Scale_Answer_Form(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return HttpResponse("Likert Answer Added")
        else:
            print form.errors
    else:
        form = Likert_Scale_Answer_Form()

    return render_to_response('add_likert_scale_answer.html', {'form': form}, context)


def add_text_answer(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = Text_Answer_Form(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return HttpResponse("Text Answer Added")
            # return render_to_response('index.html')
        else:
            print form.errors
    else:
        form = Text_Answer_Form()

    return render_to_response('add_text_answer.html', {'form': form}, context)


def add_boolean_answer(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = Boolean_Answer_Form(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return HttpResponse("Boolean Answer Added")
            # return render_to_response('index.html')
        else:
            print form.errors
    else:
        form = Boolean_Answer_Form()

    return render_to_response('add_boolean_answer.html', {'form': form}, context)


# def register(request):
#     context = RequestContext(request)
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             registered = True
#         else:
#             print user_form.errors
#     else:
#         user_form = UserForm()
#     return render_to_response(
#             'register.html',
#             {'user_form': user_form, 'registered': registered},
#             context)