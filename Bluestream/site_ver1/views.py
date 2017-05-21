# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from .models import Person, Project
from .forms import PersonForm, LoginForm, ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
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

class DashboardMainView(TemplateView):
    def get(self, request, *args, **kwargs):
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
        return render_to_response('MainForm.html', {'QT1': QT1, 'QT2': QT2})

def whatever(request):
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			u = User.objects.create_user(username = form.cleaned_data["email"], password = form.cleaned_data["password"])
			u.person.role = form.cleaned_data["role"]
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
	role = request.user.person.get_role()
	if role == 'R':
		projects = Project.objects.filter(creator = request.user)
	elif role == "C":
		projects = Project.objects.filter(client = request.user)
	role = list(request.user.person.role)[2]
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
				email = EmailMessage(proj.business_name +' - ' + proj.proj_name , 'A project has just created a project for you by your Regulatory Consultant. Go to www.bluestream.com to get started', to=[form.cleaned_data["email_recipient"]])
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
	role = request.user.person.get_role()
	if role == "R":
		project = Project.objects.filter(proj_name = name, creator = request.user)
	else:
		project = Project.objects.filter(proj_name = name, client = request.user)
	if project:
		return render(request, 'base_project.html', {'name': name})
	else:
		return HttpResponseRedirect("/dashboard")
	
