__author__ = 'alina'

# http://www.tangowithdjango.com/book/chapters/forms.html

from django import forms
import datetime
from questionnaire_site.models import Survey, Question, User, Participant,\
    Likert_Scale_Answer, Text_Answer, Boolean_Answer

# creating a form that corresponds to the Survey data model
class SurveyForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  help_text="Select Author")
    title = forms.CharField(max_length=128,
                            help_text="Enter the title of your survey!")
    description = forms.CharField(max_length=128,
                            help_text = "Briefly describe your survey")
    deadline = forms.DateField(initial=datetime.date.today(),
                               help_text="Enter the deadline for the survey")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Survey
        # Fields that we want to include in our form
        fields = ('user', 'title', 'description', 'deadline')


#  creating a form that corresponds to the Question data model
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


# creating a form that corresponds to the Participant data model
class ParticipantForm(forms.ModelForm):
    email = forms.EmailField(max_length=128, help_text="Enter participant's email")
    birth_date = forms.DateField(help_text="Enter participant's Date of Birth")
    gender = forms.ChoiceField(required=True, widget=forms.RadioSelect,
                                    choices=Participant.GENDER,
                                    help_text="Choose gender")

    class Meta:
        model = Participant
        fields = ('email', 'birth_date', 'gender')


# creating a form that corresponds to the Likert_Scale_Answer data model
class Likert_Scale_Answer_Form(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Participant.objects.all(),
                                  help_text="Select Participant",widget=forms.HiddenInput)
    question = forms.ModelChoiceField(queryset=Question.objects.filter(question_type='likert'),
                                      help_text="Select the question")
    choice = forms.ChoiceField(required=True, widget=forms.RadioSelect,
                                choices=Likert_Scale_Answer.CHOICES,
                                help_text="Choose your answer")
    class Meta:
        model = Likert_Scale_Answer
        fields = ('user', 'question', 'choice')


# creating a form that corresponds to the Text_Answer data model
class Text_Answer_Form(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Participant.objects.all(),
                                  help_text="Select Participant", widget=forms.HiddenInput)
    question = forms.ModelChoiceField(queryset=Question.objects.filter(question_type='text'),
                                      help_text="Select the question")
    text = forms.CharField(max_length=128, help_text="Enter the question's answer")

    class Meta:
        model = Text_Answer
        fields = ('user', 'question', 'text')


# creating a form that corresponds to the Boolean_Answer data model
class Boolean_Answer_Form(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Participant.objects.all(),
                                  help_text="Select Participant", widget=forms.HiddenInput)
    question = forms.ModelChoiceField(queryset=Question.objects.filter(question_type='yes / no'),
                                      help_text="Select the question")
    text = forms.BooleanField(required=False, help_text="Select Answer!",
                              widget=forms.RadioSelect(choices=[(True, 'Yes'),
                                                            (False, 'No')]))

    class Meta:
        model = Boolean_Answer
        fields = ('user', 'question', 'text')