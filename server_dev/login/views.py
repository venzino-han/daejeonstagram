# from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

from django.contrib.auth.hashers import make_password, check_password


from django.http import JsonResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist



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
            # return Response(dict(mag="No user"))
            return JsonResponse({'result': 0, 'msg': "No user"},
                                safe=False, status=status.HTTP_404_NOT_FOUND)

        if check_password(pw, user.pw):
            #return Response(dict(msg='Login success'))

            #return user id
            uid = user.id
            return JsonResponse({'result': 1, 'uid': uid, 'msg': 'Login success'},
                                status=status.HTTP_202_ACCEPTED)
        else:
            # return Response(dict(msg='Login Fail'))
            return JsonResponse({'result': 0, 'msg': 'Login Fail'},
                                safe=False, status=status.HTTP_404_NOT_FOUND)


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
            # return Response(dict(msg="Same email exist"))
            return JsonResponse({'result': 0, 'msg': 'Same email exist'},
                                safe=False, status=status.HTTP_409_CONFLICT)

        try:
            user = User.objects.create(
                userName=userName,
                userEmail=userEmail,
                pw=pw_encryted,
                gender=gender,
                birth=birth,
                userType=userType,
            )
        except:
            return JsonResponse({'result': 0, 'msg': 'Same email exist'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = UserSerializer(user)
        return JsonResponse({'result': 1, 'user': serializer.data ,  'msg': 'Sign in success'},
                                status=status.HTTP_201_CREATED)


