# from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .models import Place
# from .serializers import PlaceSerializer

# Create your views here.
@api_view(['GET'])
def helloLogin(request):
    return Response("Login API")