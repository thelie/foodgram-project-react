from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    CheckConstraint,
    DateTimeField,
    F,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    Q,
    TextField,
    UniqueConstraint,
)
from django.db.models.functions import Length
from django.forms import ValidationError

CharField.register_lookup(Length)

User = get_user_model()


def null_validator(value):
    if value < 1:
        raise ValidationError(
            ("%(value)s is not an even number"),
            params={"value": value},
        )


class Tag(Model):
    name = CharField(
        "Тэг",
        max_length=200,
        unique=True,
    )
    color = CharField(
        "Цветовой HEX-код",
        max_length=7,
        blank=True,
        null=True,
        default="FF",
    )
    slug = CharField(
        "Слаг тэга",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ("name",)
        constraints = (
            CheckConstraint(
                check=Q(name__length__gt=0),
                name="\n%(app_label)s_%(class)s_name is empty\n",
            ),
            CheckConstraint(
                check=Q(color__length__gt=0),
                name="\n%(app_label)s_%(class)s_color is empty\n",
            ),
            CheckConstraint(
                check=Q(slug__length__gt=0),
                name="\n%(app_label)s_%(class)s_slug is empty\n",
            ),
        )

    def __str__(self) -> str:
        return f"{self.name} (цвет: {self.color})"


class Ingredient(Model):
    name = CharField(
        "Ингридиент",
        max_length=200,
        unique=True,
    )
    measurement_unit = CharField(
        "Единицы измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("name",)
        constraints = (
            CheckConstraint(
                check=Q(name__length__gt=0),
                name="\n%(app_label)s_%(class)s_name is empty\n",
            ),
            CheckConstraint(
                check=Q(measurement_unit__length__gt=0),
                name="\n%(app_label)s_%(class)s_measurement_unit is empty\n",
            ),
        )

    def __str__(self) -> str:
        return f"{self.name}"


class Recipe(Model):
    author = ForeignKey(
        verbose_name="Автор рецепта",
        related_name="recipes",
        to=User,
        on_delete=CASCADE,
    )
    name = CharField(
        "Название блюда",
        max_length=200,
    )
    pub_date = DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    ingredients = ManyToManyField(
        verbose_name="Ингредиенты блюда",
        related_name="recipes",
        to=Ingredient,
        through="recipes.AmountIngredient",
    )
    tags = ManyToManyField(
        verbose_name="Тег",
        related_name="recipes",
        to="Tag",
    )
    image = ImageField("Изображение блюда", upload_to="recipe_images/")
    text = TextField("Описание блюда")
    cooking_time = PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        default=0,
        validators=(
            MinValueValidator(1, "Ваше блюдо уже готово!"),
            MaxValueValidator(600, "Очень долго ждать..."),
        ),
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)
        constraints = (
            UniqueConstraint(
                fields=("name", "author"), name="unique_for_author"
            ),
            CheckConstraint(
                check=Q(name__length__gt=0),
                name="\n%(app_label)s_%(class)s_name is empty\n",
            ),
        )

    def __str__(self) -> str:
        return f"{self.name}. Автор: {self.author.username}"

    def number_adds(self):
        return self.favorites.all().count()


class AmountIngredient(Model):
    recipe = ForeignKey(
        verbose_name="В каких рецептах",
        related_name="ingredient",
        to=Recipe,
        on_delete=CASCADE,
    )
    ingredients = ForeignKey(
        verbose_name="Связанные ингредиенты",
        related_name="recipe",
        to=Ingredient,
        on_delete=CASCADE,
    )
    amount = PositiveSmallIntegerField(
        verbose_name="Количество",
        default=0,
        validators=(
            MinValueValidator(1, "Нужно хоть какое-то количество."),
            MaxValueValidator(10000, "Слишком много!"),
        ),
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Количество ингридиентов"
        ordering = ("recipe",)
        constraints = (
            UniqueConstraint(
                fields=(
                    "recipe",
                    "ingredients",
                ),
                name="\n%(app_label)s_%(class)s ingredient alredy added\n",
            ),
        )

    def __str__(self) -> str:
        return str(self.amount)


class Subscription(Model):
    owner = ForeignKey(
        verbose_name="Подписчик",
        related_name="subscriber",
        to=User,
        on_delete=CASCADE,
    )
    author = ForeignKey(
        verbose_name="Автор",
        related_name="following",
        to=User,
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("owner",)
        constraints = (
            UniqueConstraint(
                fields=("owner", "author"),
                name="\n%(app_label)s_%(class)s_already_exist\n",
            ),
            CheckConstraint(
                check=~Q(owner=F("author")),
                name="\n%(app_label)s_%(class)s_no_self_subscribe\n",
            ),
        )

    def __str__(self) -> str:
        return f"{self.owner} --> {self.author}"


class Favorite(Model):
    owner = ForeignKey(
        verbose_name="Владелец подписки",
        related_name="favorites",
        to=User,
        on_delete=CASCADE,
    )
    recipes = ForeignKey(
        verbose_name="Понравившиеся рецепты",
        related_name="favorites",
        to="Recipe",
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = "Понравившейся рецепт"
        verbose_name_plural = "Понравившиеся рецепты"
        ordering = (
            "recipes",
            "owner",
        )
        constraints = (
            UniqueConstraint(
                fields=("owner", "recipes"),
                name="\n%(app_label)s_%(class)s recipe alredy added\n",
            ),
        )

    def __str__(self) -> str:
        return f"{self.owner}: {self.recipes}"


class ShoppingCart(Model):
    owner = ForeignKey(
        verbose_name="Владелец списка",
        related_name="shopping_cart",
        to=User,
        on_delete=CASCADE,
    )
    recipes = ForeignKey(
        verbose_name="Рецепты в корзине",
        related_name="shopping_cart",
        to=Recipe,
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = "Список рецептов в корзине"
        verbose_name_plural = "Список рецептов в корзине"
        ordering = ("owner",)
