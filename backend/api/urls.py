from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register("tags", TagViewSet)
router_v1.register("ingredients", IngredientViewSet)
router_v1.register("recipes", RecipeViewSet, "recipes")
router_v1.register("users", UserViewSet)

urlpatterns = (
    path("", include(router_v1.urls)),
    path("auth/", include("djoser.urls.authtoken")),
)
