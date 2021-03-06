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
    path('forget_password/', views.forget_password, name='forget_password'),
    path('check_email_user/', views.check_email_user, name='check_email_user'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('user_avatar_upload/', views.user_avatar_upload, name='user_avatar_upload'),
]