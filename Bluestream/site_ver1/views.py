# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
import os
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
