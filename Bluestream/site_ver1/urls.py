from django.conf.urls import url
from site_ver1 import views, models

urlpatterns = [
    # Core Pages
    url(r'^$', views.homepage, name='homepage'),
    url(r'^signup/$', views.whatever, name='submission'),
    url(r'^loginpage/$', views.loginattempt, name='login'),

    # Project dashboard pages
    url(r'^dashboard/$',  views.dashboard),
	url(r'^dashboard/newproject/$', views.newproject, name='newproject'),
	url(r'^dashboard/project/(?P<name>[^/]+)/$', views.showproject,name = 'project'),
    # 510k Sections
    url(r'^dashboard/project/(?P<name>[^/]+)/sectionlist/$',  views.dashboard_section, name='sectionlist'),
	url(r'^dashboard/project/(?P<name>[^/]+)/section3/$',   views.section3, name='section3'),
	url(r'^dashboard/project/(?P<name>[^/]+)/section4/$',   views.section4, name='section4'),
	url(r'^dashboard/project/(?P<name>[^/]+)/section5/$',   views.section5, name='section5'),
	url(r'^dashboard/project/(?P<name>[^/]+)/section6/$',   views.section6, name="section6"),
    url(r'^dashboard/project/(?P<name>[^/]+)/section7/$',   views.section7, name="section7"),
    url(r'^dashboard/project/(?P<name>[^/]+)/section8/$',   views.section8, name="section8"),
	url(r'^logout/$', views.logouttry)
]
