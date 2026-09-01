from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Admin can manage all drivers"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsDriverOwnerOrAdmin(permissions.BasePermission):
    """Driver can manage own vehicle, Admin can manage all"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.driver.user == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """Normal User cannot modify driver information"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff