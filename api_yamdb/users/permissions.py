from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ только у администраторов."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Для чтения доступно всем, для записи — только администраторам."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user and request.user.is_authenticated
                and request.user.is_admin)


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """
    Права на объект: доступ у автора, модератора или администратора.
    Используется для отзывов и комментариев.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user or request.user.is_moderator
                or request.user.is_admin)
