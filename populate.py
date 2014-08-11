# __author__ = 'alina'

# http://www.tangowithdjango.com/book/chapters/models.html

import os
import random


def add_user(username, email, first_name, last_name, password):
    u = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name,
                                   password=password)
    return u


def add_survey(user, title, description, deadline):
    s = Survey.objects.get_or_create(user=user,
                                     title=title, description=description, deadline=deadline)[0]
    return s


def add_question(question_description, survey, question_type):
    q = Question.objects.get_or_create(question_description=
                                       question_description, survey=survey, question_type=question_type)[0]
    return q


def add_participant(email, birth_date, gender):
    p = Participant.objects.get_or_create(email=email,
                                          birth_date=birth_date, gender=gender)[0]
    return p


def add_likert_scale_answer(user, question, choice):
    l_s_a = Likert_Scale_Answer.objects.get_or_create(user=user,
                                                      question=question, choice=choice)[0]
    return l_s_a


def add_text_answer(user, question, text):
    t_a = Text_Answer.objects.get_or_create(user=user,
                                            question=question, text=text)[0]
    return t_a


def add_boolean_answer(user, question, text):
    b_a = Boolean_Answer.objects.get_or_create(user=user,
                                               question=question, text=text)[0]
     # choice=choice
    return b_a


def populate():
    for i in range(2):
        s = str(i)
        add_user("user-" + s, "user-" + s, "fname" + s, "lname" + s, "1", )

    for i in range(5):
        s = str(i)
        gender = ""
        if (i % 2 == 0):
            gender += "Male"
        elif (i % 3 == 0):
            gender += "Other"
        else:
            gender += "Female"

        add_participant("participant" + s + "@gmail.com", "1987-08-05", gender)
    andrea = add_participant(email="rainbowcolours309@gmail.com", birth_date="1990-12-04", gender="Female")

    for i in range(5):
        uid = str(i / 4)
        add_survey(User.objects.get(username="user-" + uid),"Survey" + str(i), "description" + str(i), "2014-10-10")

    # BFI-10 = "10 item inventory that measures an individual on the Big Five dimensions of personality. "
    bfi_survey = add_survey(User.objects.get(username='alina'), title="BFI-10", description="I see myself as someone who... ",
                            deadline="2014-10-10")

    for i in range(50):
        if (i % 2 == 0):
            text = "likert"
        elif (i % 7 == 0):
            text = "text"
        else:
            text = "yes / no"

        add_question("What do you think of " + str(i) + "?", Survey.objects.get(title=("Survey") + str(i / 10)), text)

        add_question(question_description='... is reserved', survey=bfi_survey, question_type='likert')
        add_question(question_description='... is generally trusting', survey=bfi_survey, question_type='likert')
        add_question(question_description='... tends to be lazy', survey=bfi_survey, question_type='likert')
        add_question(question_description='... is relaxed, handles stress well', survey=bfi_survey, question_type='likert')
        add_question(question_description='... has few artistic interests', survey=bfi_survey, question_type='likert')
        add_question(question_description='... is outgoing, sociable', survey=bfi_survey, question_type='likert')
        add_question(question_description='... tends to find fault with others', survey=bfi_survey, question_type='likert')
        add_question(question_description='... does a thorough job', survey=bfi_survey, question_type='likert')
        add_question(question_description='... gets nervous easily', survey=bfi_survey, question_type='likert')
        add_question(question_description='... has an active imagination', survey=bfi_survey, question_type='likert')

    for i in range(5):
        survey = Survey.objects.get(title="Survey" + str(i))
        questions = Question.objects.filter(survey=survey)

        for question in questions:
            type = question.question_type
            pid = Participant.objects.get(email="participant" + str(i) + "@gmail.com")

            if type == "likert":
                add_likert_scale_answer(pid, question, random.randint(0, 4))

            if type == "text":
                add_text_answer(pid, question, "This is my answer")

            if type == "yes / no":
                add_boolean_answer(pid, question, bool(random.getrandbits(1)))



# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_site.settings')
    from questionnaire_site.models import Survey, Question, \
        Likert_Scale_Answer, Text_Answer, Boolean_Answer, Participant

    from django.contrib.auth.models import User

    populate()

