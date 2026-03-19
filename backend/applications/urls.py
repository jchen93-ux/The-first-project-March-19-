from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet

router = DefaultRouter()
router.register(r"applications", ApplicationViewSet, basename="applications")

urlpatterns = [
    *router.urls,
]
