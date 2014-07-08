__author__ = 'alina'

# import models
from models import Likert_Scale_Answer, Participant, Question

from django.http import HttpResponse
import logging

def add_likert_scale_answer(user, question, choice):
    l_s_a = Likert_Scale_Answer.objects.get_or_create(user=user,
                                                      question=question, choice=choice)[0]
    return l_s_a

def index(request):
    return HttpResponse("hello world!")

def viewAnswers(request):

    answer_list = Likert_Scale_Answer.objects.all()

    html_list = ""

    for answer in answer_list :
        parents = "<h3>" + answer.question.survey.title + "</h3>"
        parent_q = "<p><strong>" + answer.question.question_description + "</strong></p>"
        html_list = "<p>" + str(answer.choice) + "</p>"


    return HttpResponse("hi" + parents + parent_q + html_list)