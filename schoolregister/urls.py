from django.urls import path
from . import views

app_name = 'schoolregister'

urlpatterns = [
    path('', views.test_site, name='test_site'),
    path('nauczyciel/', views.teacher_panel, name='teacher_panel'),
    path('nauczyciel/<int:id>/', views.class_detail, name='class_detail'),
]
