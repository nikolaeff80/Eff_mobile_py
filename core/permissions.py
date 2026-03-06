from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_active:
            return False
        return request.user.user_roles.filter(role__name="admin").exists()


class HasPermission(BasePermission):
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        if not request.user or not request.user.is_active:
            return False

        return request.user.user_roles.filter(
            role__role_permissions__permission__name=self.permission_name
        ).exists()
    