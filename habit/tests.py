from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from habit.models import Habits
from django.contrib.auth import get_user_model

User = get_user_model()


class HabitsAPITests(APITestCase):
    """
    Набор тестов для проверки работы API для модели `Habits`.

    Включает тесты для создания, обновления, удаления, получения списка и получения информации о привычках.
    """

    def setUp(self):
        """
        Настройка данных для тестов.

        Создает пользователя, аутентифицирует его, и создает исходную привычку для тестирования.
        """
        self.create_url = reverse('habit:habits_create')
        self.list_url = reverse('habit:habits_list')
        self.public_list_url = reverse('habit:public_list')
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.habit = Habits.objects.create(
            owner=self.user,
            place='Стол',
            time='08:00:00',
            action='Пить воду',
            is_nice=False,
            periodicity=1,
            prize='Кофе',
            duration=2,
            is_public=False,
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=False,
            sunday=False
        )
        self.update_url = reverse('habit:habits_update', args=[self.habit.pk])
        self.delete_url = reverse('habit:habits_delete', args=[self.habit.pk])

    def test_create_habit(self):
        """
        Тест создания новой привычки.

        Проверяет успешное создание новой привычки через API. Убедитесь, что статус-код ответа 201,
        и что новая привычка успешно добавлена в базу данных.
        """
        data = {
            'place': 'Стол',
            'time': '08:00:00',
            'action': 'Пить воду',
            'is_nice': False,
            'periodicity': 1,
            'prize': 'Кофе',
            'duration': 2,
            'is_public': False,
            'monday': True,
            'tuesday': True,
            'wednesday': True,
            'thursday': True,
            'friday': True,
            'saturday': False,
            'sunday': False
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.count(), 2)
        created_habit = Habits.objects.filter(action='Пить воду').first()
        self.assertIsNotNone(created_habit)
        self.assertEqual(created_habit.action, 'Пить воду')

    def test_update_habit(self):
        """
        Тест обновления привычки.

        Проверяет успешное обновление существующей привычки через API. Убедитесь, что статус-код ответа 200,
        и что данные привычки были успешно обновлены в базе данных.
        """

        data = {
            'place': 'Стол',
            'time': '09:00:00',
            'action': 'Пить кофе',
            'is_nice': True,
            'periodicity': 2,
            'duration': 1,
            'is_public': True,
            'monday': False,
            'tuesday': False,
            'wednesday': False,
            'thursday': False,
            'friday': False,
            'saturday': True,
            'sunday': True
        }
        response = self.client.put(self.update_url, data, format='json')
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Пить кофе')

    def test_destroy_habit(self):
        """
        Тест удаления привычки.

        Проверяет успешное удаление привычки через API. Убедитесь, что статус-код ответа 204,
        и что привычка была удалена из базы данных.
        """
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.count(), 0)

    def test_list_habits(self):
        """
        Тест получения списка привычек.

        Проверяет успешное получение списка привычек через API. Убедитесь, что статус-код ответа 200,
        и что данные возвращаются в правильном формате (словарь с ключом 'results', который содержит список).
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreater(len(response.data['results']), 0)

    def test_public_list_habits(self):
        """
        Тест получения списка публичных привычек.

        Проверяет успешное получение списка публичных привычек через API. Убедитесь, что статус-код ответа 200,
        и что данные возвращаются в правильном формате (словарь с ключом 'results', который содержит список).
        """
        response = self.client.get(self.public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_retrieve_habit(self):
        """
        Тест получения информации о привычке.

        Проверяет успешное получение информации о конкретной привычке через API. Убедитесь, что статус-код ответа 200,
        и что данные о привычке возвращаются правильно.
        """
        url = reverse('habit:habits_retrieve', args=[self.habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Пить воду')
