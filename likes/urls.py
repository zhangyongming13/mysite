from django.urls import path
from . import views

urlpatterns = [
    path('like_change', views.like_change, name='like_change'),
    path('dislike_change', views.dislike_change, name='dislike_change')
]
