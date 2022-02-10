from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'schoolregister'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('nauczyciel/', views.teacher_panel, name='teacher_panel'),
    path('nauczyciel/<int:school_class_id>/', views.class_students, name='class_students'),
    path('nauczyciel/<int:school_class_id>/<int:subject_id>/', views.class_detail, name='class_detail'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('test_site/', views.test_site, name='test_site'), # sprawdzic czy da sie wyrownac
    path('test_site02/', views.test_site02, name='test_site02'),
    path('test_site03/', views.test_site03, name='test_site03'),
]
