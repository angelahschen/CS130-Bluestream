# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Django imports
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

#Other imports
import datetime
import magic

# Create your models here.
MAX_PASS_LENGTH = 20
MAX_NAME_LENGTH = 50
MAX_PROJ_LENGTH = 100

#GOOD
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
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

class FormSection3(models.Model):
    project = models.ForeignKey(Project)
    cvl     = models.CharField(max_length = 5000)

class FormSection4(models.Model):
    project = models.ForeignKey(Project)

    number = models.CharField(
            max_length      = 50,
            verbose_name    = '510K Number (if known)',
            blank           = True
    )

    device_name = models.CharField(max_length = 50)

    indication = models.CharField(
            max_length   = 5000,
            verbose_name = 'Indications for use (Describe)'
    )

class FormSection5(models.Model):
    SECTION_5_OPTIONS = (
        (None               , ''),
        ('510ksummary'      , '510K-Summary'),
        ('510kstatement'    , '510K-Statement'),
    )

    project = models.ForeignKey(Project)

    option = models.CharField(
            max_length  = 16,
            choices     = SECTION_5_OPTIONS,
            null        = True
    )

    summary = models.CharField(max_length = 5000)

class FormSection6(models.Model):
    project         = models.ForeignKey(Project)
    position        = models.CharField(max_length = 200, null=True, blank=True)
    company_name    = models.CharField(max_length = 200, null=True, blank=True)
    signature       = models.CharField(max_length = 50,  null=True, blank=True)
    submitter_name  = models.CharField(max_length = 50,  null=True, blank=True)
    date            = models.DateField(default    = datetime.date.today)
    number          = models.CharField(max_length = 50, null=True, blank=True)

class FormSection7(models.Model):
    project         = models.ForeignKey(Project)
    position        = models.CharField(max_length = 200, null=True, blank=True)
    company_name    = models.CharField(max_length = 200, null=True, blank=True)
    device_name     = models.CharField(max_length = 200, null=True, blank=True)
    certifier_name  = models.CharField(max_length = 50,  null=True, blank=True)
    device_name     = models.CharField(max_length = 50,  null=True, blank=True)
    summary_data    = models.CharField(max_length = 5000, null=True, blank=True)
    signature       = models.CharField(max_length = 50, null=True, blank=True)
    date            = models.DateField(default    = datetime.date.today)
    number          = models.CharField(max_length = 50, null=True, blank=True)

def get_cert_upload_filename(instance, filename):
    project_id      =  instance.project.id
    project_name    =  instance.project.proj_name

    return 'uploads/project_{0}_{1}/section8/cert/{2}'.format(project_id, project_name, filename)

def get_disc_upload_filename(instance, filename):
    project_id      =  instance.project.id
    project_name    =  instance.project.proj_name

    return 'uploads/project_{0}_{1}/section8/disc/{2}'.format(project_id, project_name, filename)

@deconstructible
class FileValidator(object):
    error_msg = {
        'content_type': "Files of type %(content_type)s are not allowed"
    }
    def __init__(self, content_types=()):
        self.content_types = content_types

    def __call__(self, data):
        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime = True)
            if content_type not in self.content_types:
                params ={'content_type': content_type}
                raise ValidationError(self.error_msg['content_type'], 'content_type', params)

    def __eq(self, other):
        return isinstance(other, FileValidator)


class FormSection8(models.Model):
    validate_file   = FileValidator(content_types=('application/pdf'))
    project         = models.ForeignKey(Project)
    cert_filename   = models.CharField(max_length = 50,  null=True, blank=True)
    disc_filename   = models.CharField(max_length = 50,  null=True, blank=True)
    certification   = models.FileField(upload_to = get_cert_upload_filename, verbose_name = 'Select a file', validators=[validate_file])
    disclosure      = models.FileField(upload_to = get_disc_upload_filename, verbose_name = 'Select a file', validators=[validate_file])
