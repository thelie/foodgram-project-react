from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    SerializerMethodField,
)
from django.conf import settings

User = get_user_model()


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "email", "id", "first_name", "last_name", "password")
        read_only_fields = (
            "id",
            "is_subscribed",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_username(self, username):
        if len(username) < 3:
            raise ValidationError(
                "Длина username допустима от "
                f"{settings.MIN_USERNAME_LENGTH} до {settings.MAX_CHARFIELD_LENGTH}"
            )
        if not username.isalpha():
            raise ValidationError("В username допустимы только буквы.")
        return username

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj).exists()


class UserSubscriptionsSerializer(UserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User()
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        limit = int(self.context.get("request").query_params.get("recipes_limit"))

        if not limit:
            limit = settings.PAGE_SIZE
        return obj.recipes.values("id", "name", "image", "cooking_time")[:limit]

    def get_recipes_count(self, obj):
        return obj.recipes.count
