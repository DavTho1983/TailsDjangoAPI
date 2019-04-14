from django.db import models

class Postcode(models.Model):

    name = models.CharField(max_length=50)
    postcode = models.CharField(max_length=7)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)