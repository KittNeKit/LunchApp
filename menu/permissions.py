from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsRestaurantOrIfUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS and request.user)
            or (request.user and request.user.is_staff)
            or (request.user.type_of_user == "Restaurant")
        )
