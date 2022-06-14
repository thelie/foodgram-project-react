from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.conf import settings


class User(AbstractUser):
    email = EmailField(
        verbose_name="Электронной почта",
        unique=True,
        max_length=settings.MAX_EMAIL_LENGTH,
        help_text=f"Required. <={settings.MAX_EMAIL_LENGTH} characters.",
    )
    username = CharField(
        verbose_name="Логин",
        unique=True,
        max_length=settings.MAX_CHARFIELD_LENGTH,
        help_text=f"Required. <={settings.MAX_CHARFIELD_LENGTH} characters.",
    )
    first_name = CharField(
        verbose_name="Имя",
        max_length=settings.MAX_CHARFIELD_LENGTH,
        help_text=f"Required. <={settings.MAX_CHARFIELD_LENGTH} characters.",
    )
    last_name = CharField(
        verbose_name="Фамилия",
        max_length=settings.MAX_CHARFIELD_LENGTH,
        help_text=f"Required. <={settings.MAX_CHARFIELD_LENGTH} characters.",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return f"username: {self.username}, email: {self.email}"
