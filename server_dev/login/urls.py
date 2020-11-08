from django.urls import path, include
from django.conf.urls import url
from .views import helloLogin, RegistUser, AppLogin

urlpatterns = [
    path("", helloLogin),
    path("regist_user", RegistUser.as_view(), name='register user'),
    path("app_login", AppLogin.as_view(), name='Login'),

]