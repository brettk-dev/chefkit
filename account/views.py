from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView


class RegisterAccount(CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('recipes:list')
