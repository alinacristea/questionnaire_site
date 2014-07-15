__author__ = 'alina'

from django import forms
import datetime
from questionnaire_site.models import Survey, Question, User, Participant


class SurveyForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  help_text="Select Author")
    title = forms.CharField(max_length=128,
                            help_text="Enter the title of your survey!")
    description = forms.CharField(max_length=128,
                            help_text = "Briefly describe your survey")
    deadline = forms.DateField(initial=datetime.date.today,
                               help_text="Enter the deadline for the survey")

    class Meta:
        model = Survey
        fields = ('user', 'title', 'description', 'deadline')

class QuestionForm(forms.ModelForm):
    question_description = forms.CharField(max_length=128,
                                           help_text="Enter the question")
    survey = forms.ModelChoiceField(queryset=Survey.objects.all(),
                                    help_text="Chose your survey")
    question_type = forms.ModelChoiceField(queryset=Question.QUESTION_TYPES,
                                           help_text="Chose the type of question")

    class Meta:
        model = Question
        fields = ('question_description', 'survey', 'question_type')




# class ParticipantForm(forms.ModelForm):
#     email = forms.EmailField(max_length=128, help_text="Enter your email")
#     birth_date = forms.DateField(max_length = 20)
#     gender = forms.ModelChoiceField(max_length = 18,
#                                     queryset=Participant.GENDER.all(),
#                                     help_text="Chose your gender")
#
#     class Meta:
#         model = Participant
#       fields = ...
