from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Subscription
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from .serializers import UserSerializer, UserSubscriptionsSerializer

User = get_user_model()


class CustomUserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    @action(
        methods=(
            "GET",
            "POST",
            "DELETE",
        ),
        detail=True,
    )
    def subscribe(self, request, id):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        author = get_object_or_404(User, id=id)
        serializer = UserSubscriptionsSerializer(
            author, context={"request": request}
        )

        if self.request.method in (
            "GET",
            "POST",
        ):
            obj, created = Subscription.objects.get_or_create(
                owner=user, author=author
            )
            if created:
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        if self.request.method in ("DELETE",):
            obj = get_object_or_404(Subscription, owner=user, author=author)
            obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)

    @action(methods=("GET",), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = User.objects.filter(following__owner=user)
        pages = self.paginate_queryset(authors)
        serializer = UserSubscriptionsSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
