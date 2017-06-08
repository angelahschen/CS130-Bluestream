# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.template import context
from .models import Person, Project, FormSection3, FormSection4, FormSection5, FormSection6, FormSection7, FormSection8
from .forms import PersonForm, LoginForm, ProjectForm, CoverLetterForm, Section4Form, Section5Form, Section6Form, Section7Form, Section8Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
import django.contrib.messages as messages

#Other imports
import os

#############
# Helper Functions

def get_project(request):
    if (request.user.person.role == 'R'):
        # get session project
        # TODO: do we need to revalidate the session project id? - it's server side, so it should be fine?
        project = Project.objects.filter(id      = request.session['project_id'],
                                         creator = request.user).first()
    else:
        project = Project.objects.filter(id      = request.session['project_id'],
                                         client  = request.user).first()

    return project

#############
# Section Callbacks for section_chooser in views.py

def section3(request, name):
    f = open(os.path.abspath('site_ver1/RTAdocs/QT1_1'), 'r')
    QT1_1=[]
    for line in f:
        QT1_1.append(line)
    f.close()
    f = open(os.path.abspath('site_ver1/RTAdocs/QT1_2'), 'r')
    QT1_2=[]
    for line in f:
        QT1_2.append(line)
    f.close()
    QT1 = zip(QT1_1, QT1_2)
    f = open(os.path.abspath('site_ver1/RTAdocs/QT2'), 'r')
    QT2=[]
    for line in f:
        QT2.append(line)
    f.close()
    f = open(os.path.abspath('site_ver1/RTAdocs/QT3'), 'r')
    QT3=[]
    for line in f:
        QT3.append(line)

    project = get_project(request)

    if (project is None):
        # if this is none, then the session's cached project_id isn't in any of the user's projects
        # TODO: maybe include error string saying that the session expired or something
        return redirect("/dashboard")

    previous = FormSection3.objects.filter(project = project).first()

    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            if (previous is not None):
                p = previous
            else:
                p = FormSection3()
            p = FormSection3(project = "", cvl = form.cleaned_data["cvl"])
            p.save()
    else:

        if (previous is not None):
            previous_data = {'number'       : previous.number,
                             'device_name'  : previous.device_name,
                             'indication'   : previous.indication}
        else:
            previous_data = None
        form = CoverLetterForm()

    return render(request,'Section3.html', {'form': form, 'QT1': QT1, 'QT2': QT2, 'QT3': QT3, 'name': name, 'section_name':"RTA checklist (in Section 3 after cover letter)"})

def section4(request, name):

    project = get_project(request)

    if (project is None):
        # if this is none, then the session's cached project_id isn't in any of the user's projects
        # TODO: maybe include error string saying that the session expired or something ?
        return redirect("/dashboard")

    previous = FormSection4.objects.filter(project = project).first()

    if request.method == 'POST':
        if (previous is None):
            previous = FormSection4(project = project)
        form = Section4Form(request.POST, instance = previous)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission invalid')

    else:
        form = Section4Form(instance = previous)

    context = {'form'         : form,
               'name'         : name,
               'project_id'   : request.session['project_id'],
               'section_name' : "Section 4: Indications for Use Statement"}

    return render(request,'Section4.html', context = context)

def section5(request, name):

    project = get_project(request)

    if (project is None):
        return redirect("/dashboard")

    previous = FormSection5.objects.filter(project = project).first()

    if request.method == 'POST':
        if (previous is None):
            previous = FormSection5(project = project)
        form = Section5Form(request.POST, instance = previous)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission invalid')
    else:
       form = Section5Form(instance = previous)

    context = {'form'         : form,
               'name'         : name,
               'section_name' : "Section 5: 510K Summary / 510K Statement" }

    return render(request,'Section5.html', context = context)

#form is not saving to db, query causes 500
def section6(request, name):

    project = get_project(request)

    if (project is None):
        return redirect("/dashboard")

    previous = FormSection6.objects.filter(project = project).first()

    if request.method == 'POST':
        if (previous is None):
            previous = FormSection6(project = project)
        form = Section6Form(request.POST, instance = previous)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission invalid')
    else:
        form = Section6Form(instance = previous)

    return render(request, 'Section6.html', {'form':form, 'name': name, 'section_name':"Section 6: Truthful and Accuracy Statement"})

def section7(request, name):

    project = get_project(request)

    if (project is None):
        return redirect("/dashboard")

    previous = FormSection7.objects.filter(project = project).first()

    if request.method == 'POST':
        if (previous is None):
            previous = FormSection7(project = project)
        form = Section7Form(request.POST, instance = previous)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission invalid')
    else:
        form = Section7Form(instance = previous)

    template_dev_name = form.fields['device_name'].widget.attrs['placeholder']
    if (previous is not None and previous.device_name is not None):
        template_dev_name = previous.device_name

    context = {
        'form'          : form,
        'name'          : name,
        'dev_name'      : template_dev_name,
        'section_name'  : "Section 7: Class III Summary and Certification"
    }

    return render(request, 'Section7.html', context = context)

def section8(request, name):

    project = get_project(request)

    if (project is None):
        return redirect("/dashboard")

    previous = FormSection8.objects.filter(project = project).first()

    if request.method == 'POST':

        if (previous is None):
            previous = FormSection8(project = project)

        previous.cert_filename = request.FILES['certification'].name
        previous.disc_filename = request.FILES['disclosure'].name

        form = Section8Form(data = request.POST, files = request.FILES, instance = previous)
        #TODO: check file for security
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission invalid')
    else:
        form = Section8Form()


    context = {
        'form'                      : form,
        'name'                      : name,
        'previous_certification'    : None,
        'previous_disclosure'       : None,
        'section_name'              : "Section 8: Financial Certification or Disclosure Statement" }

    if (previous is not None):
        context['previous_certification']   = previous.cert_filename
        context['previous_disclosure']      = previous.disc_filename

    return render(request, 'Section8.html', context = context)

