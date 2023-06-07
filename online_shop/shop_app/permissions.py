from rest_framework import permissions
from .config import UNSAFE_METHODS

class ReadOnlyOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, _):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        elif request.method in UNSAFE_METHODS:
            return bool(request.user and request.user.is_superuser)
        return False