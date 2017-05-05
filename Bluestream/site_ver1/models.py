# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
MAX_PASS_LENGTH = 20
MAX_NAME_LENGTH = 50
class Person(models.Model):
	name = models.CharField(max_length=MAX_NAME_LENGTH)
	password = models.CharField(max_length=MAX_PASS_LENGTH)
	email = models.EmailField(max_length=70,primary_key = True)
