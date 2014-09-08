from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from questionnaire_site import views

# the URLs created for the application
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    # when the regular expression "r'^view_survey/$'" is matched then
    # the "views.viewSurvey" function will be called
    url(r'^view_survey/$', views.viewSurvey, name='view_survey'),
    url(r'^view_answers/$', views.viewAnswers, name='view_answers'),

    url(r'^add_survey/$', views.add_survey, name='add_survey'),
    url(r'^add_question/$', views.add_question, name='add_question'),
    url(r'^add_participant/$', views.add_participant, name='add_participant'),

    url(r'^add_likert_scale_answer/$', views.add_likert_scale_answer, name='add_likert_scale_answer'),
    url(r'^add_text_answer/$', views.add_text_answer, name='add_text_answer'),
    url(r'^add_boolean_answer/$', views.add_boolean_answer, name='add_boolean_answer'),

    url(r'^add_response/$', views.add_response, name='add_response'),
    url(r'^survey_stats/$', views.survey_stats, name='survey_stats'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    # url needed to handle the AJAX request
    url(r'^delete_question/$', views.delete_question, name='delete-question'),


)

