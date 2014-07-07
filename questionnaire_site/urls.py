from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from questionnaire_site import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^view_answers/$', views.viewAnswers, name='view_answers'),
    url(r'^$', views.index, name='index'),
)