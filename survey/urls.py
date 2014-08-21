from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()

from survey.views import IndexView, ItemView, ResultView, RawResultView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^survey/$', ItemView.as_view(), name='survey'),
    url(r'^result/$', login_required(ResultView.as_view()), name='result'),
    url(r'^result/raw/$', login_required(RawResultView.as_view()),
        name='raw_result'),
    url(r'^admin/', include(admin.site.urls)),
)
