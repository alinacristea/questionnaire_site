from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from questionnaire_site import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^view_survey/$', views.viewSurvey, name='view_survey'),
    url(r'^view_answers/$', views.viewAnswers, name='view_answers'),
    url(r'^$', views.index, name='index'),
    url(r'^add_survey/$', views.add_survey, name='add_survey'),
    url(r'^add_question/$', views.add_question, name='add_question'),
    url(r'^add_participant/$', views.add_participant, name='add_participant'),

    url(r'^add_likert_scale_answer/$', views.add_likert_scale_answer, name='add_likert_scale_answer'),
    url(r'^add_text_answer/$', views.add_text_answer, name='add_text_answer'),
    url(r'^add_boolean_answer/$', views.add_boolean_answer, name='add_boolean_answer'),

    # url(r'^register/$', views.register, name='register'),


)
