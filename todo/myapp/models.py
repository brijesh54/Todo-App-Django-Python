from django.db import models

class CrudUser(models.Model):
    title = models.CharField(max_length=50,blank=True)
    status = models.CharField(max_length=2 ,blank=True)
    priority = models.IntegerField(blank=True, null=True)