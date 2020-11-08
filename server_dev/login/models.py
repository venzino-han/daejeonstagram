from django.db import models

# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=30, null=False, default=False)
    userEmail = models.CharField(max_length=30, unique=True, null=False, default=False)
    pw = models.CharField(max_length=256, null=False, default=False)
    gender = models.IntegerField()
    birth = models.CharField(max_length=20)
    userType = models.CharField(max_length=30)

    class Meta:
        db_table = 'user'
        verbose_name = 'user info table'




