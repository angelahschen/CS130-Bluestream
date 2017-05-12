# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
MAX_PASS_LENGTH = 20
MAX_NAME_LENGTH = 50
MAX_PROJ_LENGTH = 100
class Person(models.Model):
	name = models.CharField(max_length=MAX_NAME_LENGTH)
	password = models.CharField(max_length=MAX_PASS_LENGTH)
	email = models.EmailField(max_length=70,primary_key = True, blank= False)
	role = models.CharField(max_length = 50)
	phone_number = models.CharField(max_length = 12)
	

class Project(models.Model):
	proj_name = models.CharField(max_length = MAX_PROJ_LENGTH)
	business_name = models.CharField(max_length = MAX_PROJ_LENGTH)
	
class ProjectMembers(models.Model):
	project = models.ForeignKey(Project)
	person = models.ForeignKey(Person)

class Roles:
	role_name = models.CharField(max_length = MAX_NAME_LENGTH)
	