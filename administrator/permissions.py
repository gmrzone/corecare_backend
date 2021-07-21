from rest_framework.permissions import BasePermission




class IsSuperUser(BasePermission):
    message = "Only users with superuser privilege can access this page"


    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_staff and request.user.is_superuser)


class IsEmployee(BasePermission):
    message = "Only Employee can access this page"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_employee)
