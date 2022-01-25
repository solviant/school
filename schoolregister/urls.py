from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_site, name='test_site'),
]
