from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Tylko właściciel obiektu będzie miał prawo do zapisu
    """

    def has_object_permission(self, request, view, obj):
        # Odczyt dla każdego żądania przeglądarki
        if request.method in permissions.SAFE_METHODS:
            return True

        # Prawo do zapisu tylko dla właściciela obiektu
        return obj.owner == request.user