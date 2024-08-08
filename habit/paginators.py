from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Класс для настройки пагинации в API.

    Этот класс расширяет `PageNumberPagination` из Django REST Framework и
    предоставляет пользовательскую пагинацию для API. Он позволяет настраивать
    количество объектов на странице и задает максимальное количество объектов
    на странице.

    Атрибуты:
    - `page_size` (int): Количество объектов на одной странице. По умолчанию 5.
    - `page_size_query_param` (str): Параметр запроса для изменения размера страницы. По умолчанию 'page_size'.
    - `max_page_size` (int): Максимальное количество объектов на одной странице, даже если `page_size_query_param`
    установлен. По умолчанию 10.

    """
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10
