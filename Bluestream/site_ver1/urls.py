from django.conf.urls import url
from site_ver1 import views, models

urlpatterns = [
    url(r'^$',           views.HomePageView.as_view()),
    #url(r'^dashboard/mainform/$',   views.DashboardMainView.as_view()),
	url(r'^dashboard/mainform/$',   views.sections, name="dash"),
	url(r'^dashboard/section3/$',   views.section3, name="section3"),
	url(r'^dashboard/section4/$',   views.section4, name="section4"),
	url(r'^dashboard/section5/$',   views.section5, name="section5"),
    url(r'^dashboard/sectionlist/$',  views.DashboardSectionView.as_view()),
    url(r'^dashboard/$',  views.dashboard),
    url(r'^signup/$', views.whatever, name='submission'),
    url(r'^loginpage/$', views.loginattempt, name="login"),
]
