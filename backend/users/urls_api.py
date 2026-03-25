from django.urls import path
from .views_api import CsrfTokenView, LoginView, LogoutView, WhoAmIView

urlpatterns = [
    path('csrf/', CsrfTokenView.as_view(), name='auth-csrf'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('whoami/', WhoAmIView.as_view(), name='auth-whoami'),
]

