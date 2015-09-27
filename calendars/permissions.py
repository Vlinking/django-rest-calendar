from rest_framework import permissions
from calendars.models import CalendarSharing


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Checks if it is the owner
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            CalendarSharing.objects.get(calendar=obj.calendar, recipient=request.user, type='W')
        except CalendarSharing.DoesNotExist:
            shared = False
        else:
            shared = True

        return obj.calendar.owner == request.user or shared