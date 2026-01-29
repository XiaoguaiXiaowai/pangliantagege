from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet

router = DefaultRouter()
# We can register individual viewsets if we want CRUD for admin, 
# but for the public page, a single endpoint is often easier.
# However, `ResumeViewSet` is a ViewSet, so we can register it with a basename.
router.register(r'resume', ResumeViewSet, basename='resume')

urlpatterns = [
    path('', include(router.urls)),
]
