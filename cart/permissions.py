from rest_framework import permissions

class IsOwnerOrder(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
    