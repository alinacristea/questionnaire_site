__author__ = 'alina'


from django.contrib import admin
from questionnaire_site.models import Survey, Question, Participant, Likert_Scale_Answer, Text_Answer, Boolean_Answer

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Likert_Scale_Answer)
admin.site.register(Text_Answer)
admin.site.register(Boolean_Answer)
admin.site.register(Participant)
