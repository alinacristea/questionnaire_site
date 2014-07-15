__author__ = 'alina'

from models import Likert_Scale_Answer, Text_Answer, Boolean_Answer, Participant, Question, Survey


from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from questionnaire_site.forms import SurveyForm, QuestionForm

# def add_likert_scale_answer(user, question, choice):
#     l_s_a = Likert_Scale_Answer.objects.get_or_create(user=user,
#                                                       question=question, choice=choice)[0]
#     return l_s_a

def index(request):
    return HttpResponse("hello alina")

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
    # I only have answers for participant x & survey x with answers in the 20-29 range

    return render_to_response('survey.html',
                              context_dict, )

def add_survey(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return index(request)
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
            return index(request)
        else:
            print form.errors
    else:
        form = QuestionForm()

    return render_to_response('add_question.html', {'form': form}, context)

