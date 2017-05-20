# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
MAX_PASS_LENGTH = 20
MAX_NAME_LENGTH = 50
MAX_PROJ_LENGTH = 100
#GOOD
class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=MAX_NAME_LENGTH)
	password = models.CharField(max_length=MAX_PASS_LENGTH)
	email = models.EmailField(max_length=70)
	role = models.CharField(max_length = 50)
	phone_number = models.CharField(max_length = 12)
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
		
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()
	
class Project(models.Model):
	creator = models.ForeignKey(User, related_name='RC_creator')
	client = models.ForeignKey(User, related_name='Client_Assigned', blank=True, null=True)
	proj_name = models.CharField(max_length = MAX_PROJ_LENGTH)
	business_name = models.CharField(max_length = MAX_PROJ_LENGTH)
	
class ProjectMembers(models.Model):
	project = models.ForeignKey(Project)
	person = models.ForeignKey(Person)

class Roles:
	role_name = models.CharField(max_length = MAX_NAME_LENGTH)