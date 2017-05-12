from django.conf.urls import url
from site_ver1 import views, models

urlpatterns = [
    url(r'^$',           views.HomePageView.as_view()),
    url(r'^dashboard/mainform/$',   views.DashboardMainView.as_view()),
    url(r'^dashboard/sectionlist/$',  views.DashboardSectionView.as_view()),
    url(r'^dashboard/$',  views.dashboard),
    url(r'^signup/$', views.whatever, name='submission'),
    url(r'^loginpage/$', views.loginattempt, name="login"),
]
