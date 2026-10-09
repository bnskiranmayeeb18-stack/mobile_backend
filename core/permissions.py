from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "You can access only your own resources."
    def has_object_permission(self, request, view, obj):
        # for Ride: obj.user, Vehicle: obj.owner, User: obj itself
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        # For User model itself
        return obj.id == request.user.id

class IsDriver(BasePermission):
    message = "Driver role required."
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', '') == 'driver' or request.user.is_staff

class IsRider(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return obj.id == request.user.id