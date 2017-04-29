from django.conf.urls import url
from site_ver1 import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^loginpage/$', views.LoginPageView.as_view()),
    url(r'^signup/$', views.RegisterPageView.as_view()),
    url(r'^mainform$', views.MainFormView.as_view()),
]
