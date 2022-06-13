from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "id",
            "first_name",
            "last_name",
            "password"
        )
        read_only_fields = ("id",)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, username):
        if len(username) < 3:
            raise ValidationError(
                'Длина username допустима от '
                f'{3} до {150}'
            )
        if not username.isalpha():
            raise ValidationError(
                'В username допустимы только буквы.'
            )
        return username
