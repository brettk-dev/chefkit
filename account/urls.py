from django.urls import include, path

from . import views

app_name = 'account'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.RegisterAccount.as_view(), name='register'),
]
