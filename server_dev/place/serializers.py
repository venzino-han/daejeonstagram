from rest_framework import serializers
from .models import Place, Review

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('placeName', 'kakaoId', 'url', 'lat', 'lon', 'regUserId', 'body', 'timeStamp')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('kakaoId', 'userId', 'star', 'body', 'timeStamp', 'last')