from django.conf.urls import url
from site_ver1 import views, models

urlpatterns = [
    url(r'^$',  views.HomePageView.as_view()),
    url(r'^dashboard/project/(?P<name>[^/]+)/mainform/$',   views.DashboardMainView.as_view()),
    url(r'^dashboard/project/(?P<name>[^/]+)/sectionlist/$',  views.DashboardSectionView.as_view()),
    url(r'^dashboard/$',  views.dashboard),
    url(r'^signup/$', views.whatever, name='submission'),
    url(r'^loginpage/$', views.loginattempt, name="login"),
	url(r'^dashboard/newproject/$', views.newproject, name="newproject"),
	url(r'^dashboard/project/(?P<name>[^/]+)/$', views.showproject,name = "project"),
]
