from django.urls import path
from . import views

urlpatterns = [
    path('works/', views.MusicWorkList.as_view(), name='music-work-list'),
]
