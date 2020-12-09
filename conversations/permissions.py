from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, conversations):

        return bool(conversations.participants == request.user)
