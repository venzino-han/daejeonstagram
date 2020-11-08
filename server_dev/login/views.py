# from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password


# from .serializers import PlaceSerializer

# Create your views here.
@api_view(['GET'])
def helloLogin(request):
    return Response("Login API")

class AppLogin(APIView):
    def post(self, request):
        userEmail = request.query_params['userEmail']
        pw = request.query_params['pw']

        user = User.objects.filter(userEmail=userEmail).first()

        if user is None:
            return Response(dict(mag="No user"))

        if check_password(pw, user.pw):
            return Response(dict(msg='Login success'))
        else:
            return Response(dict(msg='Login Fail'))




class RegistUser(APIView):
    def post(self, request):
        userName= request.query_params['userName']
        userEmail= request.query_params['userEmail']
        pw= request.query_params['pw']
        gender= request.query_params['gender']
        birth= request.query_params['birth']
        try:
            userType= request.query_params['userType']
        except:
            userType= ''


        pw_encryted = make_password(pw)


        user = User.objects.filter(userEmail=userEmail).first()
        if user is not None:
            return Response(dict(msg="Same email exist"))

        try:
            User.objects.create(
                userName=userName,
                userEmail=userEmail,
                pw=pw_encryted,
                gender=gender,
                birth=birth,
                userType=userType,
            )
        except:
            return Response("Fail to create suer")


        data = dict(
            userName=userName,
            userEmail=userEmail,
            pw=pw_encryted,
            gender=gender,
            birth=birth,
            userType=userType,
        )

        return Response(data)


