from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.month, name='month'),
    url(r'^(?P<eventId>[-0-9]+)/hide/$', views.hide, name='hide'),
    url(r'^(?P<eventId>[-0-9]+)/done/$', views.done, name='done'),
]

