__author__ = 'alina'

# http://www.tangowithdjango.com/book/chapters/models.html

import os
import random


def add_user(username, email, firstname, lastname, password):
    u = User.objects.get_or_create(username=username, email=email, first_name=firstname, last_name=lastname,
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
    return b_a


def populate():
    for i in range(10):
        s = str(i)
        add_user("user-" + s, "user-" + s, "fname" + s, "lname" + s, "1", )

    for i in range(20):
        s = str(i)
        gender = ""
        if (i % 2 == 0):
            gender = "Male"
        elif (i % 7 == 0):
            gender = "Other"
        else:
            gender = "Female"

        add_participant("participant" + s + "@gmail.com", "1985-03-04", gender)

    for i in range(10):
        uid = str(i / 4)
        add_survey(User.objects.get(username="user-" + uid),"Survey" + str(i), "description" + str(i), "2014-10-10")

    for i in range(100):

        if (i % 2 == 0):
            text = "likert"
        elif (i % 7 == 0):
            text = "text"
        else:
            text = "yes / no"

        add_question("What do you think of " + str(i) + "?", Survey.objects.get(title=("Survey") + str(i / 10)), text)


    for i in range(10):
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

