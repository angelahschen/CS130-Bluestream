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
    url(r'^dashboard/project/delete/(?P<name>[^/]+)/$', views.deleteproject,name = 'project'),
    # 510k Sections
    url(r'^dashboard/project/(?P<name>[^/]+)/sectionlist/$',  views.dashboard_section, name='sectionlist'),
    url(r'^dashboard/project/(?P<name>[^/]+)/section(?P<section_number>[0-9]+)/$',   views.section_chooser),
    url(r'^logout/$', views.logouttry)
]
