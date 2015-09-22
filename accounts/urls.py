from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

__author__ = 'Bartek'

from django.conf.urls import url, include


urlpatterns = [
    url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url('^accounts/', include('django.contrib.auth.urls'))
]