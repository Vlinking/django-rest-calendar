from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


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