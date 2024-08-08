from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User


class UserAPITests(APITestCase):
    """
    Класс тестов для API пользовательских операций.

    Использует Django REST Framework `APITestCase` для выполнения тестов на создание, обновление,
    удаление и получение пользователей, а также для проверки доступа и аутентификации.

    Методы:
        - `setUp`: Настройка данных для тестов.
        - `get_access_token`: Получение JWT токена для аутентификации.
        - `authenticate`: Аутентификация пользователя и установка токена в заголовках.
        - `test_create_user`: Тестирование создания нового пользователя.
        - `test_update_user`: Тестирование обновления информации о пользователе.
        - `test_destroy_user`: Тестирование удаления пользователя.
        - `test_list_users_authenticated`: Тестирование получения списка пользователей для аутентифицированного
           пользователя.
        - `test_retrieve_user_authenticated`: Тестирование получения информации о пользователе для аутентифицированного
           пользователя.
    """

    def setUp(self):
        """
        Настройка данных для тестов.

        Создает начального пользователя и URL-адреса для операций обновления и удаления.
        Также устанавливает токен аутентификации для клиента.
        """
        self.create_url = reverse('users:user-register')
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.update_url = reverse('users:users-update', args=[self.user.pk])
        self.delete_url = reverse('users:users-delete', args=[self.user.pk])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())

    def get_access_token(self):
        """
        Получает JWT токен для аутентификации.

        Выполняет POST запрос к эндпоинту получения токена с заданными учетными данными
        и возвращает полученный токен доступа.

        Возвращает:
            str: JWT токен доступа.
        """
        response = self.client.post(reverse('users:token_obtain_pair'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, format='json')
        return response.data['access']

    def authenticate(self):
        """
        Аутентифицирует пользователя и устанавливает токен в заголовках.

        Получает токен доступа и устанавливает его в заголовках для последующих запросов.
        """
        token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_user(self):
        """
        Тестирование создания нового пользователя.

        Отправляет POST запрос на создание нового пользователя с заданными данными
        и проверяет, что пользователь был успешно создан и добавлен в базу данных.
        """
        url = self.create_url
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email='newuser@example.com').email, 'newuser@example.com')

    def test_update_user(self):
        """
        Тестирование обновления информации о пользователе.

        Аутентифицирует пользователя, отправляет PUT запрос для обновления информации
        о существующем пользователе и проверяет, что изменения были успешно применены.
        """
        self.authenticate()
        data = {
            'email': 'updateduser@example.com',
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName'
        }
        response = self.client.put(self.update_url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_destroy_user(self):
        """
        Тестирование удаления пользователя.

        Аутентифицирует пользователя и отправляет DELETE запрос на удаление существующего пользователя,
        затем проверяет, что пользователь был успешно удален из базы данных.
        """
        self.authenticate()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_list_users_authenticated(self):
        """
        Тестирование получения списка пользователей для аутентифицированного пользователя.

        Аутентифицирует пользователя и отправляет GET запрос для получения списка всех пользователей,
        затем проверяет, что запрос выполнен успешно и возвращает статус 200 OK.
        """
        self.authenticate()
        url = reverse('users:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_authenticated(self):
        """
        Тестирование получения информации о пользователе для аутентифицированного пользователя.

        Аутентифицирует пользователя и отправляет GET запрос для получения информации
        о конкретном пользователе, затем проверяет, что запрос выполнен успешно и возвращает статус 200 OK.
        """
        self.authenticate()
        url = reverse('users:users-get', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
