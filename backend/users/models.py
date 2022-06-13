from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField


class User(AbstractUser):
    email = EmailField(verbose_name="Электронной почта", unique=True, max_length=255)
    username = CharField(verbose_name="Логин", unique=True, max_length=100)
    first_name = CharField(verbose_name="Имя", max_length=255)
    last_name = CharField(verbose_name="Фамилия", max_length=255)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return f"username: {self.username}, email: {self.email}"
