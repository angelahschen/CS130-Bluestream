# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Person
from .forms import PersonForm, LoginForm
from django.contrib import messages 
# Create your views here.
class HomePageView(TemplateView):
	template_name = "index.html"

class LoginPageView(TemplateView):
	template_name = "loginpage.html"

class RegisterPageView(TemplateView):
	template_name = "signup.html"

class MainFormView(TemplateView):
    template_name = "MainForm.html"
	   
class DashboardView(TemplateView):
    template_name = "Dashboard.html"

def whatever(request):
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			p = Person(name = form.cleaned_data["name"], password = form.cleaned_data["password"], email = form.cleaned_data["email"])
			p.save()
			form = LoginForm()
			return HttpResponseRedirect("/loginpage")
	else:
		form = PersonForm()
	return render(request, 'signup.html', {'form': form})
		
def loginattempt(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			return redirect("/dashboard")
	else:
		form = LoginForm()
	return render(request, 'loginpage.html', {'form': form})
	
