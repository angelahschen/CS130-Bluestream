# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
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
# Create your views here.

def homepage(request):
    return render(request, 'index.html')

def dashboard_section(request):
    return render('sectionlist.html')

def section_chooser(request, name, section_number):
    '''
    select the right section to call from section_views.py
    using the section number captured in the url
    '''
    import section_views
    module_fns = dir(section_views)
    fn_name = 'section{0}'.format(section_number)
    if (fn_name not in module_fns):
        return redirect("./")
    fn = getattr(section_views, fn_name)
    return fn(request, name)

def whatever(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(username = form.cleaned_data["email"], password = form.cleaned_data["password"])
            u.person.role = form.cleaned_data["role"][0]
            u.person.name = form.cleaned_data["name"]
            u.save()
            return HttpResponseRedirect("/loginpage")
    else:
        form = PersonForm()
    return render(request, 'signup.html', {'form': form})

def loginattempt(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["email"], password = form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("/dashboard")
    else:
        form = LoginForm()
    return render(request, 'loginpage.html', {'form': form})

def logouttry(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/loginpage")

@login_required
def dashboard(request):
    role = request.user.person.role
    if role == 'R':
        projects = Project.objects.filter(creator = request.user)
    elif role == 'C':
        projects = Project.objects.filter(client = request.user)
    data = []
    request.session['project_id'] = 0 # clearing the session id
    for project in projects:
            data.append({'name': project.proj_name, 'id' : project.id})
    return render(request, 'dashboard.html', {'projects': data, 'role': role == 'R'})
@login_required
def newproject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["email_recipient"] != '':
                clients = User.objects.filter(username = form.cleaned_data["email_recipient"])
                for client in clients:
                    proj = Project(creator = request.user, proj_name = form.cleaned_data["proj_name"], business_name = form.cleaned_data["business_name"], client = client)
                email = EmailMessage(proj.business_name +' - ' + proj.proj_name , 'A project has just been created for you by your Regulatory Consultant. Go to www.bluestream.com to get started', to=[form.cleaned_data["email_recipient"]])
                email.send()
            else:
                proj = Project(creator = request.user, proj_name = form.cleaned_data["proj_name"], business_name = form.cleaned_data["business_name"])
            proj.save();
            return HttpResponseRedirect("/dashboard")
    else:
        form = ProjectForm()
    return render(request, 'newproject.html', {'form': form})

@login_required
def showproject(request, name):
    role = request.user.person.role
    project_id = int(request.GET['id'])
    if role == "R":
        project = Project.objects.filter(id = project_id, creator = request.user)
    else:
        project = Project.objects.filter(id = project_id, client = request.user)
    if project:
        request.session['project_id'] = project_id
        return render(request, 'sectionlist.html', {'name': name, 'id': project_id})
    else:
        return HttpResponseRedirect("/dashboard")

def logout_view(request):
    logout(request)


