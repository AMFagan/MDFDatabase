from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'(?P<code>[A-Za-z0-9]{5})', views.mdf_test),
]
