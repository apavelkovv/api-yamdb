from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает изменение только администратору, чтение — всем."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAdmin(permissions.BasePermission):
    """Разрешает доступ только администратору."""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff