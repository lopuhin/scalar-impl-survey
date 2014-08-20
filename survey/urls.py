from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from survey.views import IndexView, ItemView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^survey/$', ItemView.as_view(), name='survey'),
    url(r'^admin/', include(admin.site.urls)),
)
