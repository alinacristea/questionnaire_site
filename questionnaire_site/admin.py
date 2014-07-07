__author__ = 'alina'


from django.contrib import admin
from questionnaire_site.models import Survey, Question, Answer, Participant

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Participant)


