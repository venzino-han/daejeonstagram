from django.db import models
from django.apps import apps
# from login.models import User
# Create your models here.

class Place(models.Model):
    placeName = models.CharField(max_length=40, null=False, default=False)
    # PK
    kakaoId = models.CharField(max_length=40, null=False, default=False, primary_key=True)
    url = models.CharField(max_length=200)
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
    regUserId = models.ForeignKey('login.User', on_delete=models.DO_NOTHING)
    body = models.TextField()
    class Meta:
        db_table = 'place'
        verbose_name = 'place info table'
