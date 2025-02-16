from rest_framework.permissions import BasePermission


class IsAuthenticatedWithToken(BasePermission):
    """ Проверяет, передан ли JWT-токен в заголовке Authorization. """

    def has_permission(self, request, view):
        # Проверяем наличие заголовка Authorization
        auth_header = request.headers.get("Authorization")

        # Токен должен начинаться с "Bearer " и содержать значение
        if auth_header and auth_header.startswith("Bearer "):
            return True

        return False
