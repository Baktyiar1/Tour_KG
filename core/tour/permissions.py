from rest_framework import permissions
class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.is_authenticated and (request.user.is_admin or request.user.status == 2))

class IsAdminOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.is_authenticated and (request.user.is_admin or request.user.is_author))