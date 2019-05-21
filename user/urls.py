from django.urls import path
from .views import login, logout, register, login_for_medal, user_info


urlpatterns = [
    path('login/', login, name='login'),
    path('login_for_medal', login_for_medal, name='login_for_medal'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('user_info/', user_info, name='user_info'),
]