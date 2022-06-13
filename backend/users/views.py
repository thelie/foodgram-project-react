from djoser.views import UserViewSet as DjoserViewSet
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer

User = get_user_model()


class CustomUserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
