from django.urls import path
from rest_framework.authtoken import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('login/', auth_views.obtain_auth_token),
    path('register/', csrf_exempt(views.Register.as_view())),
]
