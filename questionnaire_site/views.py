__author__ = 'alina'

from models import Likert_Scale_Answer, Text_Answer, Boolean_Answer, \
    Participant, Question, Survey, Survey_Likert_Total


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from questionnaire_site.forms import SurveyForm, QuestionForm, ParticipantForm, \
    Likert_Scale_Answer_Form, Text_Answer_Form, Boolean_Answer_Form

from django.contrib.auth import authenticate, login, logout
# from django.core.mail import send_mail, BadHeaderError
from chartit import DataPool, Chart


# Create a view for the Home Page
def index(request):
    # Get the context from the HTTP request
    context = RequestContext(request)
    # query the database for a list of all surveys currently stored
    all_surveys = Survey.objects.all()
    # place the list of surveys in the context_dict dictionary which will be passed to the template
    context_dict = {'all_surveys': all_surveys}
    # render the response and send it back to the user
    return render_to_response('index.html', context_dict, context)


# Creating a view for a completed questionnaire, including the participant
# who answered the questions and their answers
def viewAnswers(request):
    context = RequestContext(request)

    survey_id = request.GET.get('survey', '')
    email_id = request.GET.get('email', '')

    # find a survey with a given survey_id retrieved before
    survey = Survey.objects.get(title=survey_id)
    # find a participant with a given email_id retrieved before
    participant = Participant.objects.get(email=email_id)
    # retrieve all the associated questions for a given survey
    questions = Question.objects.filter(survey=survey)

    list = []
    # retrieve the answers of all types of questions for a given participant
    likert_results = Likert_Scale_Answer.objects.filter(user=participant, question=questions)
    text_results = Text_Answer.objects.filter(user=participant, question=questions)
    boolean_results = Boolean_Answer.objects.filter(user=participant, question=questions)

    # add all answers and the correspondent question to an array
    for answer in likert_results:
        list.append("<p>"+ str(answer.question.question_description) + " " + str(answer.choice) + "</p>")

    for answer in text_results:
        list.append("<p>"+ str(answer.question.question_description) + " " + str(answer.text) + "</p>")

    for answer in boolean_results:
        list.append("<p>"+ str(answer.question.question_description) + " " + str(answer.text) + "</p>")

    # add the survey, participant and answers to a dictionary
    context_dict = {'likert_results': likert_results,
                    'text_results': text_results,
                    'boolean_results': boolean_results,
                    'survey': survey,
                    'participant': participant}

    return render_to_response('view_answers.html', context_dict, context)


# http://www.tangowithdjango.com/book/chapters/forms.html
# create a view to visualise an existing survey
def viewSurvey(request):
    context = RequestContext(request)
    # based on survey title get a survey
    survey_id = request.GET.get('survey', '')
    # get all surveys with a given survey_id retrieved before
    survey = Survey.objects.get(title=survey_id)
    # retrieve all questions for that survey
    questions = Question.objects.filter(survey=survey)
    # display the QuestionForm
    form = QuestionForm()
    context_dict = {'questions': questions,
                    'survey': survey,
                    'form': form}

    # is that a HTTP POST request?
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # is the form provided valid?
        if form.is_valid():
            # if yes, save the survey with the information added
            form.save(commit=True)
            return HttpResponse("done")
        else:
            # the form has errors, so print them to the terminal
            print form.errors

    return render_to_response('view_survey.html', context_dict, context)


# Create a view to add a new survey
def add_survey(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            # Save the new survey to the database.
            form.save(commit=True)
            # redirect user to that survey's web page to add questions to it
            return HttpResponseRedirect('/view_survey/?survey=' + form.cleaned_data['title'])
        else:
            print form.errors
    else:
        # If the request was not a POST, display the form
        form = SurveyForm()
    # Bad form (or form details), no form supplied...
    return render_to_response('add_survey.html', {'form': form}, context)


# Create a view to add a new question
def add_question(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # redirect to the same page to add more questions for a chosen survey
            # return HttpResponseRedirect('/add_question/')

            # redirect to the Home Page
            return HttpResponseRedirect('/')
        else:
            print form.errors
    else:
        form = QuestionForm()
    return render_to_response('add_question.html', {'form': form}, context)


# http://stackoverflow.com/questions/4198510/delete-an-object-with-ajax-jquery-in-django
# function to delete a question object using AJAX functionality
def delete_question(request):
        question = request.GET.get('question')
        question_to_delete = Question.objects.get(pk=question)
        question_to_delete.delete()

        # for likert questions, once the question is deleted I had to delete the likert total as well
        if question_to_delete.question_type == "likert":
            question_totals_to_delete = Survey_Likert_Total.objects.get(question=question_to_delete)
            question_totals_to_delete.delete()
        return HttpResponse('OK')


# Create a view to add a new participant
def add_participant(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # redirect to the Home Page
            return HttpResponseRedirect('/')
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
            form.save(commit=True)
            return HttpResponseRedirect('/')
            # return HttpResponse("Likert Answer Added")
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
            form.save(commit=True)
            return HttpResponseRedirect('/')
            # return HttpResponse("Text Answer Added")
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
            form.save(commit=True)
            return HttpResponseRedirect('/')
            # return HttpResponse("Boolean Answer Added")
        else:
            print form.errors
    else:
        form = Boolean_Answer_Form()

    return render_to_response('add_boolean_answer.html', {'form': form}, context)

# http://stackoverflow.com/questions/18489393/django-submit-two-different-forms-with-one-submit-button
# function to submit all answers for a survey
def add_response(request):
    context = RequestContext(request)
    forms = []

    if request.method == 'POST':
        forms2 = []
        invalid = False

        # this is the validation section, to check if every question belongs to the correspondent survey
        survey_toCompareWith = None
        # the range depends on the number of questions of a survey
        # here I have considered a maximum of 40 questions for a survey
        for i in range(0, 40):
            try:
                # to give each form its own name, I used the 'prefix' keyword argument
                likert_f = (Likert_Scale_Answer_Form(request.POST, prefix="likertformID" + str(i)))
                if likert_f.is_valid():
                    question_des = (likert_f.cleaned_data['question'])
                    question = (Question.objects.get(question_description=question_des))
                    survey = question.survey.title

                    if survey_toCompareWith==None:
                        survey_toCompareWith=survey

                    elif survey_toCompareWith != survey:
                        print("Questions are from different surveys!")
                        invalid = True
                    forms2.append(likert_f)
                else:
                    print("invalid likert_form")
                    invalid = True
            # catching any possible error
            except:
                # we pass any errors caught
                pass

            try:
                text_f = (Text_Answer_Form(request.POST, prefix="textformID" + str(i)))
                if text_f.is_valid():
                    question_des = (text_f.cleaned_data['question'])
                    question = (Question.objects.get(question_description=question_des))
                    survey = question.survey.title

                    if survey_toCompareWith==None:
                        survey_toCompareWith=survey

                    elif survey_toCompareWith != survey:
                        print("Questions are from different surveys!")
                        invalid = True
                    forms2.append(text_f)
                else:
                    print("invalid text_form")
                    invalid = True
            except:
                pass

            try:
                boolean_f = (Boolean_Answer_Form(request.POST, prefix="boolformID" + str(i)))
                if boolean_f.is_valid():
                    question_des = (boolean_f.cleaned_data['question'])
                    question = (Question.objects.get(question_description=question_des))
                    survey = question.survey.title

                    if survey_toCompareWith==None:
                        survey_toCompareWith=survey

                    elif survey_toCompareWith != survey:
                        print("Questions are from different surveys!")
                        invalid = True
                    forms2.append(boolean_f)
                else:
                    print("invalid boolean_form")
                    invalid = True
            except:
                pass

        # if every form is valid, then we save it with the new data added
        if invalid==False:
            for form in forms2:
                form.save(commit = True)
            return HttpResponse("Added response!")
        else:
            return HttpResponse("Failed to Add Response!")

    # what if the request is not POST
    # just display all the forms details
    else:
        survey_id = request.GET.get('survey', '')
        survey = Survey.objects.get(title=survey_id)

        email_id = request.GET.get('email', '')
        participant = Participant.objects.get(email=email_id)

        likert_question = Question.objects.filter(question_type='likert', survey=survey)
        text_question = Question.objects.filter(question_type='text', survey=survey)
        boolean_question = Question.objects.filter(question_type='yes / no', survey=survey)

        count = 0
        for question in likert_question:

            data = {'user': participant, 'question': question}
            # I used 'initial' to declare the initial values for the form fields: participant and question
            f = Likert_Scale_Answer_Form(initial=data, prefix="likertformID"+str(count))
            forms.append(f)
            count += 1

        for question in text_question:
            data = {'user': participant, 'question': question}
            f = Text_Answer_Form(initial=data, prefix="textformID"+str(count))
            forms.append(f)
            count += 1

        for question in boolean_question:
            data = {'user': participant, 'question': question}
            f = Boolean_Answer_Form(initial=data, prefix="boolformID" + str(count))
            forms.append(f)
            count += 1

        context_dict = {'likert_question': likert_question,
                        'text_question': text_question,
                        'boolean_question': boolean_question,
                        'forms': forms,
                        'survey': survey,
                        'participant': participant,
        }

    return render_to_response('add_response.html', context_dict, context)


# http://www.tangowithdjango.com/book/chapters/login.html
# Create a view for login functionality
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

# http://www.tangowithdjango.com/book/chapters/login.html
# Create a view for logout functionality
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


# http://127.0.0.1:8000/survey_stats/?survey=Survey0
# adding charts functionality for the likert_scale answers
# http://chartit.shutupandship.com/demo/chart/column-chart/
def survey_stats(request):
    survey_id = request.GET.get('survey', '')
    survey = Survey.objects.get(title=survey_id)

    likert_questions = Question.objects.filter(question_type="likert", survey=survey)

    # variables
    likert_question_names = []
    charts = []
    chartLoadString = " "
    count = 1
    participant_number = 0

    for question in likert_questions:

        chartLoadString += "container" + str(count) + ","
        likert_answers = Likert_Scale_Answer.objects.filter(question=question)
        likert_question_names.append(question.question_description + "<hr>")

        participant_number = likert_answers.count()

        # create a DataPool with the data we want to display
        ds = DataPool(
            series=
            [{'options': {
                'source': Survey_Likert_Total.objects.filter(question=question).order_by("choice_id")},
              'terms': [
                  'choice_id', 'total', 'choice_text']}
            ])
        # create the chart object
        cht = Chart(
            datasource=ds,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': False},
              'terms': {
                  'choice_text': [
                      'total']
              }}],
            chart_options=
            {'title': {
                'text': question.question_description},
             'xAxis': {
                 'reversed': False,
                 'title': {
                     'text': 'Likert Answers'
                 }
             },
             'yAxis': {
                 'reversed': False},
            }
        )

        count += 1
        charts.append(cht)

        for likert_answer in likert_answers:
            likert_question_names.append("<p>" + str(likert_answer.choice) + "</p>")

    context_dict = {"charts":charts,
                    "chartnumber": chartLoadString,
                    "survey": survey,
                    "participant_number":participant_number}

    # send the chart object, currently in the dictionary, to the template
    return render_to_response('survey_stats.html', context_dict)



# https://docs.djangoproject.com/en/dev/topics/email/#preventing-header-injection
# https://docs.djangoproject.com/en/1.3/topics/email/

# def send_email(request):
#     subject = request.POST.get('Complete the following survey', '')
#     message = request.POST.get('Please click the link below and follow the instructions', '')
#     from_email = request.POST.get('rainbowcolours309@gmail.com', '')
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['alina.andreea.cristea@gmail.com'],  fail_silently=False)
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect("/")
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')