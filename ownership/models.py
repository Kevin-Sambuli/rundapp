# from djgeojson.fields import PolygonField
from django.db import models
from django.conf import settings
from parcels.models import Parcels
import datetime


class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=False,
                              null=False, default=None)
    parcel = models.OneToOneField(Parcels, blank=False, verbose_name='Parcels', null=False, on_delete=models.CASCADE,
                                  related_name="land_parcel", related_query_name="land_parcel")
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ownership'
        verbose_name_plural = "ownership"

    # def __str__(self):
    #     return self.username.title()
