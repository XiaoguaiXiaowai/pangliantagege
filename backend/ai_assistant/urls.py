from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.rag_health_check, name='rag_health_check'),
]