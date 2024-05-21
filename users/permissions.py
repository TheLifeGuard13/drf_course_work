from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj) -> bool:
        if obj.owner == request.user:
            return True
        return False


class IsStaff(permissions.BasePermission):
    """Проверяет является ли пользователь staff."""

    def has_permission(self, request, view) -> bool:
        if request.user.is_staff:
            return True
        return False
