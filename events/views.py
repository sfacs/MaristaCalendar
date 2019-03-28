# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from pip._internal import logger
from pip._internal.utils import logging

from events.models import Event


def index(request):
    events = Event.objects.order_by('-date').exclude(hidden=True)
    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)


def month(request, year, month):
    events = Event.objects.order_by('-date') \
        .exclude(hidden=True) \
        .filter(date__range=[year + "-" + month + "-01", year + "-" + month + "-31"])

    days = calendar.monthrange(int(year), int(month))[1]
    context = {
        'events': events,
        'month': month,
        'year': year,
        'days': range(1, days + 1)
    }
    return render(request, 'events/month.html', context)


def done(request, eventId):
    event = get_object_or_404(Event, pk=eventId)
    event.done = True
    event.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    next = request.GET.get('next')
    return HttpResponseRedirect(next)


def hide(request, eventId):
    event = get_object_or_404(Event, pk=eventId)
    event.hidden = True
    event.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    next = request.GET.get('next')
    return HttpResponseRedirect(next)
