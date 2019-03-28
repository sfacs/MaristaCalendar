# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Event(models.Model):
    eventId = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=10)
    date = models.DateTimeField()
    description = models.TextField()
    hidden = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.date.strftime("%d/%m/%y") + " " + self.title

