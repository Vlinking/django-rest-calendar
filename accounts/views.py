from django.contrib.auth.models import User
from django.views.generic import TemplateView

from rest_framework import viewsets, permissions

from accounts import models


class ProfileView(TemplateView):
    """
    Profile view after a successful login
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'username': self.request.user.username
        })
        return context


class CalendarUserAdminViewSet(viewsets.ModelViewSet):
    """
    Convenience API view for viewing all data for the admin
    and all operations
    """
    queryset = models.CalendarUser.objects.all()
    serializer_class = models.CalendarUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserAdminViewSet(viewsets.ModelViewSet):
    """
    Convenience API view for viewing all data for the admin
    and all operations
    """
    queryset = User.objects.all()
    serializer_class = models.UserSerializer
    permission_classes = (permissions.IsAdminUser,)

