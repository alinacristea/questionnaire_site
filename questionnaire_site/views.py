__author__ = 'alina'

# import models
from models import Answer

from django.http import HttpResponse
import logging

def index(request):
    return HttpResponse("hello world!")

def viewAnswers(request):

    answer_list = Answer.objects.all()

    html_list = ""

    for answer in answer_list :
        parents = "<h3>" + answer.question_answer.survey.title + "</h3>"
        parent_q = "<p><strong>" + answer.question_answer.question_description + "</strong></p>"
        html_list = "<p>" + answer.choice + "</p>"


    return HttpResponse("hi" + parents + parent_q + html_list)