# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Person
from .forms import PersonForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
import os
# Create your views here.
class HomePageView(TemplateView):
	template_name = "index.html"

class LoginPageView(TemplateView):
	template_name = "loginpage.html"

class RegisterPageView(TemplateView):
	template_name = "signup.html"

class MainFormView(TemplateView):
        #template_name = "MainForm.html"
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
	   
class DashboardView(TemplateView):
    template_name = "Dashboard.html"

class DashboardSectionView(TemplateView):
	template_name = "sectionlist.html"

class DashboardMainView(TemplateView):
	template_name = "test-main.html"

def whatever(request):
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			p = Person(name = form.cleaned_data["name"], password = form.cleaned_data["password"], email = form.cleaned_data["email"])
			p.save()
			u = User.objects.create_user(username = form.cleaned_data["email"], password = form.cleaned_data["password"])
			u.save()
			form = LoginForm()
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
	print(form)
	return render(request, 'loginpage.html', {'form': form})
	
@login_required
def dashboard(request):
	return render(request, 'dashboard.html', {})
