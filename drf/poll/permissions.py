from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom Permission to allow only owners of an object to perform a
    destructive operation

    Parent Class:
        BasePermission: all django custom permissions must inherit from
                    this class 
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user