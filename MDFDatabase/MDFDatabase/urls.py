from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [

    path('admin/', admin.site.urls),
    path('modules', views.module_index),
    url(r'modules/(?P<code>[A-Za-z0-9]{5})', views.mdf_test),
    path('staff', views.staff_index),
    url(r'staff/(?P<id_number>\d+)', views.staff_member),
    path('courses', views.course_index),
    url(r'courses/(?P<level>[A-Za-z]+)_(?P<shorthand>[A-Za-z]+)', views.course)
]
