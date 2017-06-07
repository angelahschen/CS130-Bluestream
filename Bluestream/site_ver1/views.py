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
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            p = FormSection3(project = "", cvl = form.cleaned_data["cvl"])
            p.save()
    else:
        form = CoverLetterForm()

    return render(request,'Section3.html', {'form': form, 'QT1': QT1, 'QT2': QT2, 'name': name, 'section_name':"RTA checklist (in Section 3 after cover letter)"})

def section4(request, name):
    # TODO: do we need to revalidate the session project id? - it's server side, so it should be fine?
    project = Project.objects.filter(id      = request.session['project_id'],
                                     creator = request.user).first()
    if (project is None):
        # if this is none, then the session's cached project_id isn't in any of the user's projects
        # TODO: maybe include error string saying that the session expired or something
        return redirect("/dashboard")

    previous = FormSection4.objects.filter(project = project).first()

    if request.method == 'POST':
        form = Section4Form(request.POST)
        if form.is_valid():
            if (previous is not None):
                p = previous
            else:
                p = FormSection4()

            p.project     = project
            p.number      = form.cleaned_data['number']
            p.device_name = form.cleaned_data['device_name']
            p.indication  = form.cleaned_data['indication']
            p.save()

    else:
        if (previous is not None):
            previous_data = {'number'       : previous.number,
                             'device_name'  : previous.device_name,
                             'indication'   : previous.indication}
        else:
            previous_data = None
        form = Section4Form(initial = previous_data)

    return render(request,'Section4.html', {'form': form,'name': name, 'section_name':"Section 4: Indications for Use Statement"})

def section5(request, name):
    if request.method == 'POST':
        form = Section5Form(request.POST)
        if form.is_valid():
            p = FormSection5(project = "", summary = form.cleaned_data["summary"])
            p.save()
    else:
       form = Section5Form()
    return render(request,'Section5.html', {'form': form, 'name': name, 'section_name':"Section 5: 510K Summary / 510K Statement" })

#form is not saving to db, query causes 500
def section6(request, name):
	if request.method == 'POST':
		form = Section6Form(request.POST)
		print form.errors
		if form.is_valid():
			p = FormSection6(project = "", position = form.cleaned_data["position"], company_name = form.cleaned_data["company_name"], submitter_name = form.cleaned_data["certifier_name"], date = form.cleaned_data["date"], no_510k = form.cleaned_data["number"])
			#p = FormSection6(project = Project.objects.get(proj_name=name), position = form.cleaned_data["position"], company_name = form.cleaned_data["company_name"], submitter_name = form.cleaned_data["submitter_name"], date = form.cleaned_data["date"], no_510k = form.cleaned_data["number"])
			p.save();
			#messages.success(request, 'Form submission successful')
			#return HttpResponseRedirect(p.get_absolute_url()+'/')
		#else:
			#messages.error(request, 'Form submission invalid')
	else:
		form = Section6Form()
	return render(request, 'Section6.html', {'form':form, 'name': name, 'section_name':"Section 6: Truthful and Accuracy Statement"})

def section7(request, name):
	if request.method == 'POST':
		form = Section7Form(request.POST)
		if form.is_valid():
			p = FormSection7(project = "", position = form.cleaned_data["position"], company_name = form.cleaned_data["company_name"], certifier_name = form.cleaned_data["certifier_name"], device_name = form.cleaned_data["device_name"], summary_data = form.cleaned_data["summary_data"], date = form.cleaned_data["date"], no_510k = form.cleaned_data["number"])
			p.save();
	else:
		form = Section7Form()
	return render(request, 'Section7.html', {'form':form, 'name': name, 'section_name':"Section 7: Class III Summary and Certification"})

def section8(request, name):
	if request.method == 'POST':
		form = Section8Form(request.POST, request.FILES)
		if form.is_valid():
			p = FormSection7(project = "", certification = form.cleaned_data["certification"], disclosure = form.cleaned_data["disclosure"])
			p.save()
	else:
		form = Section8Form()
	return render(request, 'Section8.html', {'form':form, 'name': name, 'section_name':"Section 8: Financial Certification or Disclosure Statement" })

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


