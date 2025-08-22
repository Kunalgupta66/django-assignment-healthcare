from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of a Patient to view/edit it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id
