from django.conf.urls import url
from site_ver1 import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^login/$', views.LoginPageView.as_view()),
    url(r'^register/$', views.RegisterPageView.as_view()),
]
