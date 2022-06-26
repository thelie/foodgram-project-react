# Generated by Django 4.0 on 2022-01-19 11:48

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Обязательно для заполнения. Максимум 254 букв.",
                        max_length=254,
                        unique=True,
                        verbose_name="Адрес электронной почты",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text="Обязательно для заполнения. От 3 до 150 букв.",
                        max_length=150,
                        unique=True,
                        validators=[
                            users.validators.MinLenValidator(min_len=3),
                            users.validators.OneOfTwoValidator(),
                        ],
                        verbose_name="Уникальный юзернейм",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Обязательно для заполнения.Максимум 150 букв.",
                        max_length=150,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        help_text="Обязательно для заполнения.Максимум 150 букв.",
                        max_length=150,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        help_text="Обязательно для заполнения.Максимум 150 букв.",
                        max_length=150,
                        verbose_name="password",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "subscribe",
                    models.ManyToManyField(
                        related_name="subscribers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Подписка",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ("username",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name="myuser",
            constraint=models.CheckConstraint(
                check=models.Q(("username__length__gte", 3)),
                name="\nusername too short\n",
            ),
        ),
    ]
