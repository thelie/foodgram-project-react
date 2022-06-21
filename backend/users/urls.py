from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

app_name = "users"

router_v1 = DefaultRouter()
router_v1.register(prefix="users", viewset=CustomUserViewSet, basename="users")

urlpatterns = (
    path("", include(router_v1.urls)),
    path("auth/", include("djoser.urls.authtoken")),
)
