__author__ = 'alina'

from django import forms
import datetime
from questionnaire_site.models import Survey, Question, User, Participant, Likert_Scale_Answer


class SurveyForm(forms.ModelForm):
    # user will need to be authenticate @TODO
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  help_text="Select Author")
    title = forms.CharField(max_length=128,
                            help_text="Enter the title of your survey!")
    description = forms.CharField(max_length=128,
                            help_text = "Briefly describe your survey")
    deadline = forms.DateField(initial=datetime.date.today(),
                               help_text="Enter the deadline for the survey")

    class Meta:
        model = Survey
        fields = ('user', 'title', 'description', 'deadline')


class QuestionForm(forms.ModelForm):
    question_description = forms.CharField(max_length=128,
                                           help_text="Enter the question")
    survey = forms.ModelChoiceField(queryset=Survey.objects.all(),
                                    help_text="Choose your survey")
    question_type = forms.ChoiceField(required=True, widget=forms.RadioSelect,
                                      choices=Question.QUESTION_TYPES,
                                        help_text="Choose the type of question")

    class Meta:
        model = Question
        fields = ('question_description', 'survey', 'question_type')

class ParticipantForm(forms.ModelForm):
    email = forms.EmailField(max_length=128, help_text="Enter your email")
    birth_date = forms.DateField(
                    help_text="Enter your Date of Birth")
    gender = forms.ChoiceField(required=True, widget=forms.RadioSelect,
                                    choices=Participant.GENDER,
                                    help_text="Choose your gender")

    class Meta:
        model = Participant
        fields = ('email', 'birth_date', 'gender')

#         in my 'models' the choice is an IntegerField

# class Likert_Scale_Answer_Form(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.all(),
#                                   help_text="Select User/participant")
#     question = forms.ModelChoiceField(queryset=Question.objects.filter(question_type = 'likert'),
#                                       help_text="Select the question")
#     choice = forms.IntegerField(required=True, widget=forms.RadioSelect,
#                                 # choices=Likert_Scale_Answer.CHOICES,
#                                 help_text="Choose your answer")
#     class Meta:
#         model = Likert_Scale_Answer
#         fields = ('user', 'question', 'choice')

# choice = models.IntegerField(max_length=2, choices=CHOICES)
