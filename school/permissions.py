from rest_framework import permissions
from users.models import UserRoles


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
