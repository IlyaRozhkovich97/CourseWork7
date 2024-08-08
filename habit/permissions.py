from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.

    Проверяет, является ли текущий пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет разрешение для объекта.

        :param request: Объект запроса.
        :param view: Представление, к которому относится запрос.
        :param obj: Объект, для которого проверяются разрешения.
        :return: True, если текущий пользователь является владельцем объекта, иначе False.
        """
        return obj.owner == request.user
