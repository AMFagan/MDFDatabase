"""mdf_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('modules/', views.mdf_index),
    url(r'modules/(?P<code>[A-Za-z0-9]{5})/$', views.mdf_test),
    url(r'modules/(?P<code>[A-Za-z0-9]{5})/pdf/', views.mdf_pdf),
    url(r'modules/(?P<code>[A-Za-z0-9]{5})/duties/', views.duties_module),
    path('staff/', views.staff_index),
    path('staff/all_surname/', views.all_staff_surname),
    path('staff/all_hours/', views.all_staff_hours),
    url(r'staff/(?P<personnel_id>\d+)', views.staff_member),
    path('courses/', views.course_index),
    url(r'courses/(?P<code>[A-Za-z0-9]+)/$', views.course),
    url(r'courses/(?P<code>[A-Za-z0-9]+)/(?P<year>[1234589])$', views.course_year),
    url(r'courses/(?P<code>[A-Za-z0-9]+)/schedule', views.course_schedule),
    path('predecessors/', views.pre_index),
    url(r'predecessors/(?P<code>[A-Za-z0-9]{5})', views.dependancies),
    path('successors/', views.succ_index),
    url(r'successors/(?P<code>[A-Za-z0-9]{5})', views.successors),
    path('duties/', views.duty_index),
]