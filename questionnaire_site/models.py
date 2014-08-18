__author__ = 'alina'

# http://www.tangowithdjango.com/book/chapters/models.html

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ObjectDoesNotExist

# class that represents a singular survey
class Survey(models.Model):
    user = models.ForeignKey(User, verbose_name="Author")
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)
    deadline = models.DateField(null=True)

    # https://docs.djangoproject.com/en/dev/ref/forms/validation/
    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow deadline to be before current date @TODO date picker
        if self.deadline < datetime.date.today():
            raise ValidationError("Deadlines cannot be in the past")

    # The __unicode()__ method is used to provide a unicode representation of a model instance.
    def __unicode__(self):
        return (self.title)

# class that represents a question
class Question(models.Model):
    TEXT = 'text'
    LIKERT = 'likert'
    BOOLEAN = 'yes / no'
    QUESTION_TYPES = ((LIKERT, 'likert'),
                      (TEXT, 'text'),
                      (BOOLEAN, 'yes / no')
    )
    question_description = models.CharField(max_length=128)
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=128, choices=QUESTION_TYPES)

    # override the save method
    def save(self, *args, **kwargs):
        # save the Question model as it is
        super(Question, self).save(*args, **kwargs)
        # instantiate the totals, starting with 0
        Survey_Likert_Total.objects.create(question=self, total=0, choice_id=0,
                                           choice_text="1 Strongly disagree")
        Survey_Likert_Total.objects.create(question=self, total=0, choice_id=1,
                                           choice_text="2 Disagree")
        Survey_Likert_Total.objects.create(question=self, total=0, choice_id=2,
                                           choice_text="3 Neither agree nor disagree")
        Survey_Likert_Total.objects.create(question=self, total=0, choice_id=3,
                                           choice_text="4 Agree")
        Survey_Likert_Total.objects.create(question=self, total=0, choice_id=4,
                                           choice_text="5 Strongly agree")

    def __unicode__(self):
        return (self.question_description)

# class that represents a participant
class Participant(models.Model):
    # what if they change their email @TODO
    email = models.EmailField(max_length=128, null=False, unique=True)
    birth_date = models.DateField(max_length=128, null=False)
    GENDER = (
        ('Male', 'male'),
        ('Female', 'female'),
        ('Other', 'other'),
    )
    gender = models.CharField(max_length=128, choices=GENDER)
    # validated_email = models.BooleanField() @TODO
    def __unicode__(self):
        return (self.email)

# class that represents a likert-scale answer
class Likert_Scale_Answer(models.Model):
    user = models.ForeignKey(Participant)
    question = models.ForeignKey(Question, limit_choices_to={'question_type': 'likert'})
    CHOICES = (
        (0, 'Strongly Disagree'),
        (1, 'Disagree'),
        (2, 'Neither agree nor disagree'),
        (3, 'Agree'),
        (4, 'Strongly Agree') )
    choice = models.IntegerField(max_length=2, choices=CHOICES)

    def save(self, *args, **kwargs):
        current_total = 0
        choice_text = ""
        try:
            question1 = Survey_Likert_Total.objects.get(question=self.question, choice_id=self.choice)
            current_total = question1.total
            # deleting previous object then recreating it with +1 added to the previous total
            question1.delete()

        except ObjectDoesNotExist :
            print("does not exist!!!")

        if self.choice == 0:
            choice_text = "1 Strongly disagree"
        if self.choice == 1:
            choice_text = "2 Disagree"
        if self.choice == 2:
            choice_text = "3 Neither agree nor disagree"
        if self.choice == 3:
            choice_text = "4 Agree"
        if self.choice == 4:
            choice_text = "5 Strongly agree"

        Survey_Likert_Total.objects.create(question=self.question,total=current_total+1,choice_id=self.choice,choice_text=choice_text)

        super(Likert_Scale_Answer, self).save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow users to answer previously answered questions
        a_list = (Likert_Scale_Answer.objects.filter(user=self.user))

        for answer in a_list:
            if answer.question == self.question:
                raise ValidationError("You may not answer the same question more than once.")

    def __unicode__(self):
        return str(self.CHOICES[self.choice]) + " - " + self.user.email

# class that represents a text answer
class Text_Answer(models.Model):
    user = models.ForeignKey(Participant)
    question = models.ForeignKey(Question, limit_choices_to={'question_type': 'text'})
    text = models.CharField(max_length=128)

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't allow users to answer previously answered questions
        a_list = (Text_Answer.objects.filter(user=self.user))

        for answer in a_list:
            if answer.question == self.question:
                raise ValidationError("You may not answer the same question more than once.")

    def __unicode__(self):
        return (self.text)

# class that represents a boolean answer
class Boolean_Answer(models.Model):
    user = models.ForeignKey(Participant)
    question = models.ForeignKey(Question, limit_choices_to={'question_type': 'yes / no'}, null=False, blank=False,)
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

# class to represent all likert-scale responses
class Survey_Likert_Total(models.Model):
    question = models.ForeignKey(Question)
    total = models.IntegerField(default=0)
    choice_id = models.IntegerField()
    choice_text = models.TextField()

    def __unicode__(self):
        return (self.question.question_description + " " + " choice " + str(self.choice_id) +
                " " + "total " + str(self.total))