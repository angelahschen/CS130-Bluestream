# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.template import context
from .models import Person, Project, FormSection3, FormSection4, FormSection5
from .forms import PersonForm, LoginForm, ProjectForm, CoverLetterForm, Section4Form, Section5Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

class LoginPageView(TemplateView):
    template_name = "loginpage.html"

class RegisterPageView(TemplateView):
    template_name = "signup.html"

class DashboardView(TemplateView):
    template_name = "Dashboard.html"

class DashboardSectionView(TemplateView):
    template_name = "sectionlist.html"

class DashboardSection3View(TemplateView):
	template_name = "Section3.html"

class DashboardSection4View(TemplateView):
	template_name = "Section4.html"

class DashboardSection5View(TemplateView):
	template_name = "Section5.html"

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
	
	return render(request,'Section3.html', {'form': form, 'QT1': QT1, 'QT2': QT2, 'name': name, 'section_name':"Section 3: RTA Checklist"})

def section4(request, name):
	if request.method == 'POST':
		form = Section4Form(request.POST)
		if form.is_valid():
			p = FormSection4(project = "", number = form.cleaned_data["number"], device_name= form.cleaned_data["device_name"], indication = form.cleaned_data["indication"])
			p.save()
	else:
		form = Section4Form()
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
	
#TODO: consider using django.contrib.auth.mixins.LoginRequiredMixin	
@login_required
def dashboard(request):
	role = request.user.person.role
	if role == 'R':
		projects = Project.objects.filter(creator = request.user)
	elif role == "C":
		projects = Project.objects.filter(client = request.user)
	data = []
	for project in projects:
		data.append({'name': project.proj_name})
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
	if role == "R":
		project = Project.objects.filter(proj_name = name, creator = request.user)
	else:
		project = Project.objects.filter(proj_name = name, client = request.user)
	if project:
		return render(request, 'sectionlist.html', {'name': name})
	else:
		return HttpResponseRedirect("/dashboard")

def logout_view(request):
    logout(request)

	
