__author__ = 'alina'

from models import Likert_Scale_Answer, Text_Answer, Boolean_Answer, Participant, Question, Survey

from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from questionnaire_site.forms import SurveyForm, QuestionForm, ParticipantForm
    #  Likert_Scale_Answer_Form

# def add_likert_scale_answer(user, question, choice):
#     l_s_a = Likert_Scale_Answer.objects.get_or_create(user=user,
#                                                       question=question, choice=choice)[0]
#     return l_s_a

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
    # I only have answers for participant x & survey x with answers in the x0-x9 range (9, 9, [90-99])

    return render_to_response('survey.html',
                              context_dict, )

def viewSurvey(request):
    survey_id = request.GET.get('survey', '') # based on survey title
    survey = Survey.objects.get(title=survey_id)
    questions = Question.objects.filter(survey=survey)

    context_dict = {'questions': questions,
                    'survey': survey,}
    return render_to_response('survey.html',
                              context_dict, )

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
            return HttpResponse("Created Survey")
            # return index(request)
        else:
            print form.errors
    else:
        form = SurveyForm()

    return render_to_response('add_survey.html', {'form': form}, context)



'''
def decode_url(str):
    return str.replace('_', ' ')

def encode_url(str):
    return str.replace(' ', '_')

def get_survey_list(max_results=0, starts_with=''):
    survey_list = []
    if starts_with:
        survey_list = Survey.objects.filter(name__startswith=starts_with)
    else:
        survey_list = Survey.objects.all()

    if max_results > 0:
        if (len(survey_list) > max_results):
            survey_list = survey_list[:max_results]

    for survey in survey_list:
        survey.url = encode_url(survey.title)

    return survey_list



def add_question(request, category_name_url):
    context = RequestContext(request)

    survey_title = decode_url(category_name_url)
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            question = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Survey.objects.get(name=survey_title)
                question.survey = cat
            except Survey.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('add_category.html', {}, context)



            # With this, we can then save our new model instance.
            question.save()

            # Now that the page is saved, display the category instead.
            return survey_title(request, category_name_url)
        else:
            print form.errors
    else:
        form = QuestionForm()

    return render_to_response( 'add_page.html',
            {'category_name_url': category_name_url,
             'survey_title': survey_title, 'form': form},
             context)


'''

def add_question(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
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
            return HttpResponse("Participant Added")
            # return index(request)
        else:
            print form.errors
    else:
        form = ParticipantForm()

    return render_to_response('add_participant.html', {'form': form}, context)

'''
def add_likert_scale_answer(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = Likert_Scale_Answer_Form(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return index(request)
        else:
            print form.errors
    else:
        form = Likert_Scale_Answer_Form()

    return render_to_response('add_likert_scale_answer.html', {'form': form}, context)
'''

