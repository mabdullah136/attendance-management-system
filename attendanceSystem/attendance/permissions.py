from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    """
    Custom permission to allow only Admins or Managers to create/update attendance.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["Admin", "Manager", "Super Admin", "Employee", "HR"]
