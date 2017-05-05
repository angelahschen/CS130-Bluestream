# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from site_ver1.models import Person
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
	p = Person(name = request.POST.get("contactname"), password = request.POST.get("password"), email = request.POST.get("contactemail"))
	pass_one = request.POST.get("password")
	pass_two = request.POST.get("rpassword")
	print(pass_one, pass_two)
	if pass_one != pass_two:
		return render(
			request,
			'signup.html',
			context={'message':"Passwords did not match!"},
		)
	else:
		return render(
			request,
			'signup.html',
			context={'message': "Account created successfully"},
		)
