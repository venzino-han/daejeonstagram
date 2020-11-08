from django.urls import path
from .views import helloLogin

urlpatterns = [
    path("", helloLogin),
]