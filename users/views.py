from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from users.serializers import UserSerializer
from rest_framework import generics


class UserCreateAPIView(generics.CreateAPIView):
    """
    API представление для создания нового пользователя.

    Использует сериализатор `UserSerializer` для валидации и создания нового пользователя.

    Переопределяет метод `perform_create` для установки пароля пользователя и его активации.

    Атрибуты:
        - `serializer_class` (UserSerializer): Сериализатор для валидации и создания пользователя.
        - `queryset` (QuerySet): Набор всех пользователей.
        - `permission_classes` (list): Список классов разрешений, позволяющих доступ без аутентификации (AllowAny).
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Сохраняет нового пользователя, устанавливает пароль и активирует его.

        Параметры:
            serializer (UserSerializer): Сериализатор с валидированными данными пользователя.

        Метод сохраняет пользователя, устанавливает его пароль и активирует его,
        затем сохраняет изменения в базе данных.
        """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """
    API представление для получения списка всех пользователей.

    Использует сериализатор UserSerializer для отображения информации о пользователях.

    Требует аутентификации.

    Атрибуты:
        serializer_class (UserSerializer): Сериализатор для отображения пользователей.
        queryset (QuerySet): Набор всех пользователей.
        permission_classes (list): Список классов разрешений, требующий аутентификации.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveView(generics.RetrieveAPIView):
    """
    API представление для получения информации об одном пользователе.

    Использует сериализатор UserSerializer для отображения информации о пользователе.

    Требует аутентификации.

    Атрибуты:
        serializer_class (UserSerializer): Сериализатор для отображения пользователя.
        queryset (QuerySet): Набор всех пользователей.
        permission_classes (list): Список классов разрешений, требующий аутентификации.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    API представление для обновления информации о пользователе.

    Использует сериализатор UserSerializer для валидации и обновления пользователя.

    Требует аутентификации.

    Атрибуты:
        serializer_class (UserSerializer): Сериализатор для валидации и обновления пользователя.
        queryset (QuerySet): Набор всех пользователей.
        permission_classes (list): Список классов разрешений, требующий аутентификации.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    API представление для удаления пользователя.

    Использует сериализатор UserSerializer для удаления пользователя.

    Требует аутентификации.

    Атрибуты:
        serializer_class (UserSerializer): Сериализатор для удаления пользователя.
        queryset (QuerySet): Набор всех пользователей.
        permission_classes (list): Список классов разрешений, требующий аутентификации.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
