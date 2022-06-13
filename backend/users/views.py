from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
