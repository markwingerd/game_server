from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to write (POST, PUT, DELETE).
    Everyone can read (GET).
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests for anyone
        if request.method in SAFE_METHODS:
            return True
        # Require authentication for all other methods
        return request.user and request.user.is_authenticated