# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
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

class DashboardSectionView(TemplateView):
	template_name = "sectionlist.html"

class DashboardMainView(TemplateView):
	template_name = "test-main.html"
