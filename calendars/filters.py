from rest_framework import filters

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter for getting only owned objects
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
