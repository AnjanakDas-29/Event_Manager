from rest_framework import permissions
from .models import UserProfile




class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                if request.method in permissions.SAFE_METHODS:
                    return True
                return profile.role == 'Admin'
            except UserProfile.DoesNotExist:
                return False
        return False