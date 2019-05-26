from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_for_medal', views.login_for_medal, name='login_for_medal'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('change_user_password/', views.change_user_password, name='change_user_password'),
]