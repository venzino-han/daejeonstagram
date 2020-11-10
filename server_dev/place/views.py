
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from .models import Place
from .serializers import PlaceSerializer

from django.http import JsonResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from login.models import User


class PlaceManage(APIView):

    def get(self, request):
        kakaoId = request.query_params['kakaoId']
        place = Place.objects.filter(kakaoId=kakaoId).first()
        if not place :
            return JsonResponse({'result': 0, 'msg': "No place"},
                                safe=False, status=status.HTTP_404_NOT_FOUND)
        place = PlaceSerializer(place)
        return JsonResponse({'result': 1, 'place': place.data, 'msg': 'Place found'},
                            safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        uid = int(request.query_params['regUserId'])
        user = User.objects.filter(id=uid).first()
        if not user:
            return JsonResponse({'result': 0, 'msg': "No user"},
                                        safe=False, status=status.HTTP_404_NOT_FOUND)

        kakaoId = request.query_params['kakaoId']
        place = Place.objects.filter(kakaoId=kakaoId).first()
        if place :
            return JsonResponse({'result': 0, 'msg': 'Same place exist'},
                                safe=False, status=status.HTTP_409_CONFLICT)

        try:
            placeData = dict(request.GET.items())
            placeData['regUserId'] = user
            # print(placeData)
            place = Place(**placeData)
            place.save()
            place = PlaceSerializer(place)

            return JsonResponse({'result': 1, 'place': place.data ,'msg': 'Place register success'},
                                    safe=False, status=status.HTTP_201_CREATED)

        except:
            return JsonResponse({'result': 0, 'msg': 'Place add error'},
                                safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
