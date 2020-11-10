from django.urls import path, include
from django.conf.urls import url
from .views import PlaceManage, ReviewManage

urlpatterns = [
    path("", PlaceManage.as_view()),
    path("review/", ReviewManage.as_view()),
]