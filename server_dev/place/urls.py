from django.urls import path, include
from django.conf.urls import url
from .views import PlaceManage

urlpatterns = [
    path("", PlaceManage.as_view())
]