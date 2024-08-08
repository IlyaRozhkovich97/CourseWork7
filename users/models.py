from django.db import models
from django.contrib.auth.models import AbstractUser
from users.management.commands.csu import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Модель пользовательских данных в системе.

    Эта модель расширяет стандартную модель пользователя Django (AbstractUser)
    и заменяет поле `username` на `email` в качестве основного поля для аутентификации.

    Поля:
    - email (EmailField): Адрес электронной почты пользователя. Должен быть уникальным.
    - phone (CharField): Телефонный номер пользователя. Необязательное поле.
    - city (CharField): Город пользователя. Необязательное поле.
    - avatar (ImageField): Аватар пользователя. Загружается в каталог `users/avatars`. Необязательное поле.
    - telegram_chat_id (CharField): Идентификатор чата. Необязательное поле.
    - country (CharField): Страна проживания пользователя. Необязательное поле.
    - nickname (CharField): Никнейм пользователя. Должен быть уникальным.

    Атрибуты:
    - USERNAME_FIELD (str): Поле, которое используется для аутентификации. В этом случае это `email`.
    - REQUIRED_FIELDS (list): Список обязательных полей при создании суперпользователя. Пустой список означает,
    что не требуется дополнительных полей.

    Менеджеры:
    - objects (CustomUserManager): Менеджер для управления пользовательскими объектами, с пользовательскими методами.

    Метаданные:
    - verbose_name (str): Человекочитаемое имя модели в единственном числе.
    - verbose_name_plural (str): Человекочитаемое имя модели во множественном числе.

    Методы:
    - __str__(): Возвращает строковое представление объекта пользователя, основанное на адресе электронной почты.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=25, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=25, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", **NULLABLE)
    telegram_chat_id = models.CharField(max_length=255, verbose_name="telegram_chat_id", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    nickname = models.CharField(max_length=50, verbose_name='никнейм', unique=True, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"
