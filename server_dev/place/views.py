
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from .models import Place, Review
from .serializers import PlaceSerializer, ReviewSerializer

from django.http import JsonResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Avg

from .crud import  *

from login.models import User


class PlaceManage(APIView):
# get Place by id
    def get(self, request):
        kakaoId = request.query_params['kakaoId']
        # place = Place.objects.filter(kakaoId=kakaoId).first()
        place = read(Place,{'kakaoId':request.query_params['kakaoId']})
        if not place :
            return JsonResponse({'result': 0, 'msg': "No place"},
                                safe=False, status=status.HTTP_404_NOT_FOUND)
        place = PlaceSerializer(place)
        return JsonResponse({'result': 1, 'place': place.data, 'msg': 'Place found'},
                            safe=False, status=status.HTTP_200_OK)
# post place
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
            place = Place(**placeData)
            place.save()
            place = PlaceSerializer(place)

            return JsonResponse({'result': 1, 'place': place.data ,'msg': 'Place register success'},
                                    safe=False, status=status.HTTP_201_CREATED)

        except:
            return JsonResponse({'result': 0, 'msg': 'Place add error'},
                                safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewManage(APIView):
    # check place exist
    def checkPlace(self, request):
        kakaoId = request.query_params['kakaoId']
        place = Place.objects.filter(kakaoId=kakaoId).first()
        if not place:
            return JsonResponse({'result': 0, 'msg': "No place"},
                                safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            return False

    # get review by place id
    def get(self, request):
        kakaoId = request.query_params['kakaoId']
        pcheck = self.checkPlace(request)
        if pcheck :
            return pcheck

        #get all review
        reviews = Review.objects.filter(kakaoId=kakaoId)
        data =[ ReviewSerializer(x).data for x in reviews ]

        return JsonResponse({'result': 1, 'place': data , 'msg': 'All review'},
                            safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        # get uid and add review
        #set flag : object exist or not
        edit = 0

        #check user
        uid = int(request.query_params['userId'])
        user = User.objects.filter(id=uid).first()
        if not user:
            return JsonResponse({'result': 0, 'msg': "No user"},
                                        safe=False, status=status.HTTP_404_NOT_FOUND)

        #check place exist
        kakaoId = request.query_params['kakaoId']
        place = Place.objects.filter(kakaoId=kakaoId).first()
        if not place :
            return JsonResponse({'result': 0, 'msg': 'No place'},
                                safe=False, status=status.HTTP_404_NOT_FOUND)

        # # user already submit review --> change edit mode
        # lastReview = Review.objects.filter(kakaoId=place, userId=user, last=1).first()
        # if lastReview:
        #     edit = 1
        #     lastReview.last=0
        #     lastReview.save()

        try:
            reviewData = dict(request.GET.items())
            reviewData['userId'] = user
            reviewData['kakaoId'] = place
            reviewData['star'] = float(request.query_params['star'])
            reviewData['last'] = 1
            review = Review(**reviewData)
            review.save()
            review = ReviewSerializer(review)

            return JsonResponse({'result': 1, 'edit': edit,
                                'review': review.data,
                                'msg': 'Place review register success'},
                                safe=False, status=status.HTTP_201_CREATED)

        except:
            return JsonResponse({'result': 0, 'msg': 'Place review add error'},
                                safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import requests
from .recommend import *

class RecommendPlace(APIView):

    # get recommendable place based on user position
    # userId lat lon
    # def __init__(self):
    #     with open('./kakaoKey.txt', 'r') as f:
    #         self.rest_api_key = f.read().strip()

    def get(self, request):
        x = request.query_params['x']
        y = request.query_params['y']
        key = request.query_params['key']

        datas = getNearPlace(x ,y ,key)

        ids = [ d['id'] for d in datas ]

        placeInDB = []
        places = Place.objects.filter(kakaoId__in=set(ids))
        for p in places :
            #get stars of each items
            placeInDB.append(p)

        if len(placeInDB) > 0:
            # get stars
            stars=[]
            for p in placeInDB:
                pid = p.kakaoId
                star = Review.objects.filter(kakaoId=pid)\
                    .aggregate(Avg('star'))['star__avg']

                print([pid, star])
                if star and star >= 3:
                    stars.append([pid, round(star,2)])

            if stars != []:
                stars = sorted(stars, key= lambda x: x[1])
                return JsonResponse({'result': 1, 'rdbdata': stars, 'kakaoData': datas ,'msg': 'Check Place'},
                                    safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'result': 0, 'data': datas, 'msg': 'No stared place in DB'},
                                    safe=False, status=status.HTTP_200_OK)

        else :
            return JsonResponse({'result': 0, 'data': datas ,'msg': 'No place in DB'},
                          safe = False, status = status.HTTP_200_OK)


    #get user satisfaction for the recommendation
    # recoId, point(0-5)
    # def post(self, request):
    #     pass