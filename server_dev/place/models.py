from django.db import models
from django.utils import timezone

class Place(models.Model):
    placeName = models.CharField(max_length=40, null=False, default=False)
    # PK
    kakaoId = models.CharField(max_length=40, null=False, default=False, primary_key=True)
    url = models.CharField(max_length=200)
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
    regUserId = models.ForeignKey('login.User', on_delete=models.DO_NOTHING)
    body = models.TextField()
    timeStamp = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'place'
        verbose_name = 'place info table'

class Review(models.Model):
    kakaoId = models.ForeignKey(Place, on_delete=models.DO_NOTHING)
    userId = models.ForeignKey('login.User', on_delete=models.DO_NOTHING)
    star = models.FloatField(null=False)
    body = models.TextField()
    timeStamp = models.DateTimeField(default=timezone.now)
    last = models.IntegerField()
    class Meta:
        db_table = 'review'
        verbose_name = 'place review table'


