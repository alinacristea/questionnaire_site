__author__ = 'alina'

# import models
from models import Likert_Scale_Answer, Text_Answer, Boolean_Answer, Participant, Question, Survey

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import logging
import urlparse

def add_likert_scale_answer(user, question, choice):
    l_s_a = Likert_Scale_Answer.objects.get_or_create(user=user,
                                                      question=question, choice=choice)[0]
    return l_s_a

def index(request):
    return HttpResponse("hello world!")

def viewAnswers(request):

    surveyid = request.GET.get('survey', '')
    emailid = request.GET.get('email', '')

    survey = Survey.objects.get(title=surveyid)

    participant = Participant.objects.get(email=emailid)
    questions = Question.objects.filter(survey=survey)

    list = []

    likertresults = Likert_Scale_Answer.objects.filter(user=participant, question=questions)
    textresults = Text_Answer.objects.filter(user=participant, question=questions)
    booleanresults = Boolean_Answer.objects.filter(user=participant, question=questions)

    for answer in likertresults:
        list.append("<p>"  + str(answer.question.question_description) + " " + str(answer.choice) + "</p>")

    for answer in textresults:
        list.append("<p>"  + str(answer.question.question_description) + " " + str(answer.text) + "</p>")

    for answer in booleanresults:
        list.append("<p>"  + str(answer.question.question_description) + " " + str(answer.text) + "</p>")
    # answer = Likert_Scale_Answer.objects.get(user=participant, question=question)
    # list.append("<p>" + (answer) + "</p>")



    # http://127.0.0.1:8000/view_answers/?survey=Survey4&email=partici4@gmail.com

    return HttpResponse(str(list))
    # return render_to_response('survey.html')
