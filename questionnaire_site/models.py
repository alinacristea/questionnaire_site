__author__ = 'alina'

from django.db import models
from django.contrib.auth.models import User
import datetime


class Survey(models.Model):
    user = models.ForeignKey(User, verbose_name="Author")
    title = models.CharField(max_length=400, unique=True)
    description = models.TextField(max_length=400)
    deadline = models.DateField(null=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow deadline to be before current date
        if self.deadline < datetime.date.today():
            raise ValidationError("Deadlines cannot be in the past")

    def __unicode__(self):
        return (self.title)


class Question(models.Model):
    TEXT = 'text'
    LIKERT = 'likert'
    BOOLEAN = 'yes / no'
    QUESTION_TYPES = ((LIKERT, 'likert'),
                      (TEXT, 'text'),
                      (BOOLEAN, 'yes / no')
    )
    question_description = models.TextField(max_length=128)
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES)

    def __unicode__(self):
        return (self.question_description)


class Participant(models.Model):
    # what if they change their email @TODO
    email = models.EmailField(max_length=128, null=False, unique=True)
    birth_date = models.DateField(max_length=20, null=False)
    GENDER = (
        ('Male', 'male'),
        ('Female', 'female'),
        ('Other', 'other'),
    )
    gender = models.CharField(max_length=128, choices=GENDER)
    # validated = models.BooleanField() @TODO
    def __unicode__(self):
        return (self.email)


class Likert_Scale_Answer(models.Model):
    user = models.ForeignKey(Participant)
    question = models.ForeignKey(Question, limit_choices_to={'question_type': 'likert'})
    CHOICES = (
        (1, 'Strongly Disagree'),
        (2, 'Disagree'),
        (3, 'Neither agree nor disagree'),
        (4, 'Agree'),
        (5, 'Strongly Agree') )
    choice = models.IntegerField(max_length=2, choices=CHOICES)

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow users to answer previously answered questions
        a_list = (Likert_Scale_Answer.objects.filter(user=self.user))

        for answer in a_list:
            if answer.question == self.question:
                raise ValidationError("You may not answer the same question more than once.")

    def __unicode__(self):
        return str(self.CHOICES[self.choice])

class Text_Answer(models.Model):
    user = models.ForeignKey(Participant)
    question = models.ForeignKey(Question, limit_choices_to={'question_type': 'text'})
    text = models.TextField(max_length=512)

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow users to answer previously answered questions
        a_list = (Text_Answer.objects.filter(user=self.user))

        for answer in a_list:
            if answer.question == self.question:
                raise ValidationError("You may not answer the same question more than once.")

    def __unicode__(self):
        return (self.text)

class Boolean_Answer(models.Model):
    user = models.ForeignKey(Participant)
    question = models.ForeignKey(Question, limit_choices_to={'question_type': 'yes / no'},null=False,blank=False)

    text = models.BooleanField(verbose_name="agree")

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow users to answer previously answered questions
        a_list = (Boolean_Answer.objects.filter(user=self.user))

        for answer in a_list:
            if answer.question == self.question:
                raise ValidationError("You may not answer the same question more than once.")

    def __unicode__(self):
        if self.text == True:
            return ("yes")
        else:
            return ("no")