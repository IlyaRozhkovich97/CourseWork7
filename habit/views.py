from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from habit.models import Habits
from habit.paginators import CustomPagination
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer
from habit.services import create_periodic_task, disable_periodic_task
from django.shortcuts import render

import os
import subprocess
from django.http import HttpResponse
from django.conf import settings


class HabitsCreateAPIView(generics.CreateAPIView):
    """
    Создание новой привычки для авторизованного пользователя.

    **URL:** `habit/habits/create/`

    **Метод:** `POST`

    **Авторизация:** Требуется аутентификация пользователя.

    **Тело запроса:**

    ```json
    {
        "place": "Стол",
        "time": "08:00:00",
        "action": "Пить воду",
        "is_nice": false,
        "related": null,
        "periodicity": 1,
        "prize": "Кофе",
        "duration": 2,
        "is_public": false,
        "monday": true,
        "tuesday": true,
        "wednesday": true,
        "thursday": true,
        "friday": true,
        "saturday": false,
        "sunday": false
    }
    ```

    **Ответ:**

    - **Код 201** - Создано. Привычка успешно создана.
    - **Код 400** - Неверный запрос. Поля запроса не соответствуют требованиям.

    **Примечание:** После создания привычки также создается периодическая задача для напоминания пользователю.
    """

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Сохраняет новую привычку, устанавливает владельца и создает периодическую задачу.

        Параметры:
            serializer (HabitSerializer): Сериализатор с валидированными данными привычки.
        """
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

        hour = habit.time.hour
        minute = habit.time.minute
        week_list = [
            index for index, day in enumerate(
                [habit.monday, habit.tuesday, habit.wednesday, habit.thursday,
                 habit.friday, habit.saturday, habit.sunday]
            ) if day
        ]

        message = f"Я буду {habit.action} в {habit.place} в {habit.time}"
        create_periodic_task(
            self.request.user.username, habit.pk, hour, minute, week_list,
            message, self.request.user.telegram_chat_id
        )


class HabitsListAPIView(generics.ListAPIView):
    """
    Получение списка привычек авторизованного пользователя.

    **URL:** `habit/habits/list/`

    **Метод:** `GET`

    **Авторизация:** Требуется аутентификация пользователя.

    **Параметры запроса:**

    - `page` - Номер страницы для пагинации.

    **Ответ:**

    - **Код 200** - Успешный запрос. Возвращает список привычек текущего пользователя.

    **Формат ответа:**

    ```json
    [
        {
            "id": 1,
            "place": "Стол",
            "time": "08:00:00",
            "action": "Пить воду",
            "is_nice": false,
            "related": null,
            "periodicity": 1,
            "prize": "Кофе",
            "duration": 2,
            "is_public": false,
            "monday": true,
            "tuesday": true,
            "wednesday": true,
            "thursday": true,
            "friday": true,
            "saturday": false,
            "sunday": false,
            "created_at": "2024-08-01T12:00:00Z",
            "updated_at": "2024-08-01T12:00:00Z"
        }
    ]
    ```

    **Пагинация:** 5 привычек на странице.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает набор данных привычек для текущего пользователя.

        Возвращает:
            QuerySet: Набор привычек, принадлежащих текущему пользователю.
        """
        return Habits.objects.filter(owner=self.request.user)


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр деталей выбранной привычки пользователя.

    **URL:** `habit/habits/<int:pk>/`

    **Метод:** `GET`

    **Авторизация:** Требуется аутентификация пользователя и право собственности на привычку.

    **Ответ:**

    - **Код 200** - Успешный запрос. Возвращает данные о привычке.
    - **Код 404** - Привычка не найдена.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        """
        Возвращает набор данных привычек для текущего пользователя.

        Возвращает:
            QuerySet: Набор привычек, принадлежащих текущему пользователю.
        """
        return Habits.objects.filter(owner=self.request.user)


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление выбранной привычки пользователя.

    **URL:** `habit/habits/update/<int:pk>/`

    **Метод:** `PUT` / `PATCH`

    **Авторизация:** Требуется аутентификация пользователя и право собственности на привычку.

    **Тело запроса:** (аналогично `HabitsCreateAPIView`)

    **Ответ:**

    - **Код 200** - Успешное обновление.
    - **Код 400** - Неверный запрос. Поля запроса не соответствуют требованиям.
    - **Код 404** - Привычка не найдена.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        """
        Возвращает набор данных привычек для текущего пользователя.

        Возвращает:
            QuerySet: Набор привычек, принадлежащих текущему пользователю.
        """
        return Habits.objects.filter(owner=self.request.user)


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление выбранной привычки пользователя.

    **URL:** `habit/habits/delete/<int:pk>/`

    **Метод:** `DELETE`

    **Авторизация:** Требуется аутентификация пользователя и право собственности на привычку.

    **Ответ:**

    - **Код 204** - Успешное удаление.
    - **Код 404** - Привычка не найдена.
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        """
        Возвращает набор данных привычек для текущего пользователя.

        Возвращает:
            QuerySet: Набор привычек, принадлежащих текущему пользователю.
        """
        return Habits.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        """
        Удаляет привычку и отключает периодическую задачу, связанную с ней.

        Параметры:
            instance (Habits): Привычка, которую необходимо удалить.
        """
        disable_periodic_task(self.request.user.username, instance.pk)
        super().perform_destroy(instance)


class HabitsPublicListAPIView(generics.ListAPIView):
    """
    Получение списка публичных привычек.

    **URL:** `habit/habits/public/`

    **Метод:** `GET`

    **Авторизация:** Открыто для всех.

    **Параметры запроса:**

    - `page` - Номер страницы для пагинации.

    **Ответ:**

    - **Код 200** - Успешный запрос. Возвращает список публичных привычек.

    **Формат ответа:** (аналогично `HabitsListAPIView`)

    **Пагинация:** 5 привычек на странице.
    """

    serializer_class = HabitSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает набор публичных привычек.

        Возвращает:
            QuerySet: Набор публичных привычек.
        """
        return Habits.objects.filter(is_public=True)


def home(request):
    """
    Главная страница проекта.
    """
    return render(request, 'habit/home.html')


def run_tests(request):
    # Путь к manage.py
    manage_py = os.path.join(settings.BASE_DIR, 'manage.py')

    # Запуск тестов для приложения users
    result_users = subprocess.run([settings.PYTHON_BIN, manage_py, 'test', 'users'], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    output_users = result_users.stdout.decode('utf-8') + result_users.stderr.decode('utf-8')

    # Запуск тестов для приложения habit
    result_habit = subprocess.run([settings.PYTHON_BIN, manage_py, 'test', 'habit'], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    output_habit = result_habit.stdout.decode('utf-8') + result_habit.stderr.decode('utf-8')

    # Объединение результатов
    full_output = f"Users Tests:\n{output_users}\n\nHabit Tests:\n{output_habit}"

    # Вывод результатов в HTTP-ответе
    return HttpResponse(f"<pre>{full_output}</pre>")
