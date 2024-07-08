from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Пользовательский класс разрешений, который позволяет только владельцам объекта
    просматривать или редактировать его, а другим пользователям только просматривать.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # Разрешить PUT, PATCH, DELETE запросы только владельцам объекта.
        return obj.author.user == request.user
