from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, comment):

        return bool(comment.post.user == request.user)


class MyText(BasePermission):
    def has_object_permission(self, request, view, text):

        return bool(text.user == request.user)