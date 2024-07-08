from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(unique=True)
    anomaly_score = models.FloatField()

class Item(models.Model):
    item_id = models.IntegerField(unique=True)
    anomaly_score = models.FloatField()