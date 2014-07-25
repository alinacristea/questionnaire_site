__author__ = 'alina'

from models import Likert_Scale_Answer, Text_Answer, Boolean_Answer, Participant, Question, Survey


from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from questionnaire_site.forms import SurveyForm, QuestionForm, ParticipantForm, \
    Likert_Scale_Answer_Form, Text_Answer_Form, Boolean_Answer_Form\
    # , UserForm

from django.contrib.auth import authenticate, login, logout

# Create a view for the Home Page
def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)

# Creating a view for a completed questionnaire, including the participant who answered the questions and their answers
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
# http://www.tangowithdjango.com/book/chapters/forms.html
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

# Create a view to add a new survey
def add_survey(request):
    # Get the context from the request.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():


            # user = form.cleaned_data['user']
            # title = form.cleaned_data['title']
            # description = form.cleaned_data['description']
            # deadline = form.cleaned_data['deadline']
            # Survey.objects.create(user=user, title=title, description=description, deadline=deadline)


            # Save the new survey to the database.
            form.save(commit = True)
            return HttpResponseRedirect('/view_survey/?survey=' + form.cleaned_data['title'])
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SurveyForm()
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('add_survey.html', {'form': form}, context)

# Create a view to add a new question
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

# Create a view to add a new participant
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

# Create a view to add a likert-scale answer
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

# Create a view to add a text answer
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

# Create a view to add a boolean answer
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

# http://www.tangowithdjango.com/book/chapters/login.html - Create a view for login functionality
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

# http://www.tangowithdjango.com/book/chapters/login.html - Create a view for logout functionality
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


