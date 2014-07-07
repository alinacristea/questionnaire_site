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
    #TEXT = 'text'
    LIKERT_SCALE = 'likert-scale, select only 1 of the 5 options provided'
    QUESTION_TYPES = ((LIKERT_SCALE, 'likert-scale'),
   # (TEXT, 'text'),
    )
    question_description = models.TextField(max_length=128)
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(
        max_length=200, choices=QUESTION_TYPES)

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


class Answer(models.Model):
    user = models.ForeignKey(Participant)
    question_answer = models.ForeignKey(Question)
    CHOICES = (
        ('1', 'Strongly Disagree'),
        ('2', 'Disagree'),
        ('3', 'Neither agree nor disagree'),
        ('4', 'Agree'),
        ('5', 'Strongly Agree') )
    choice = models.CharField(max_length=1, choices=CHOICES)

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow users to answer previously answered questions
        a_list = (Answer.objects.filter(user=self.user))


        for answer in a_list:
            if answer.question_answer == self.question_answer:
                raise ValidationError("Participants may not answer the same question more than once.")

    def __unicode__(self):
        return (self.choice)




