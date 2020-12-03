from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, follow_relation):

        return bool(follow_relation.follower == request.user)
