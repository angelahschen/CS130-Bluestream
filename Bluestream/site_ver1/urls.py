from django.conf.urls import url
from site_ver1 import views, models

urlpatterns = [
    url(r'^$',           views.HomePageView.as_view()),
    url(r'^mainform$',   views.MainFormView.as_view()),
    url(r'^dashboard$',  views.DashboardView.as_view()),
	url(r'^signup$', views.whatever, name='submission'),
	url(r'^loginpage$', views.loginattempt, name="login"),
]
