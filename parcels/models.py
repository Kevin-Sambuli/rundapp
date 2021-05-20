# from django.db import models
from django.contrib.gis.db import models
import datetime
from django.conf import settings
from django.template.defaultfilters import date


# Create your models here.
class Parcels(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)
    perimeter = models.FloatField()
    area_ha = models.FloatField()
    lr_no = models.CharField(max_length=10)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'parcels'
        verbose_name_plural = "parcels"

    def __str__(self):
        return self.lr_no

    @property
    def popup_content(self):
        popup = "<span>Parcel ID   :  </span>{}".format(self.id)
        popup += "<span>Owner      :  </span>{}".format(self.owner)
        popup += "<span>Perimeter  :  </span>{}".format(self.perimeter)
        popup += "<span>Area (m)   :  </span>{}".format(self.area_ha)
        popup += "<span>Plot Number:  </span>{}".format(self.lr_no)
        return popup


# model representing parcel details
class ParcelDetails(models.Model):
    AGRICULTURAL = 'agricultural'
    RESIDENTIAL = 'residential'
    COMMERCIAL = 'commercial'
    LANDUSE = [
        (AGRICULTURAL, 'Agricultural'),
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial'),
    ]
    FREEHOLD = 'freehold'
    LEASEHOLD = 'leasehold'
    TENURE = [
        (FREEHOLD, 'Freehold'),
        (LEASEHOLD, 'Leasehold'),
    ]

    parcel = models.OneToOneField(Parcels, blank=False, verbose_name='Parcels', null=False, on_delete=models.CASCADE,
                                  related_name="details", related_query_name="details")
    land_use = models.CharField('Landuse', max_length=15, choices=LANDUSE, default=RESIDENTIAL, blank=False, null=False)
    tenure = models.CharField('Tenure', max_length=10, choices=TENURE, default=FREEHOLD, blank=False, null=False)
    purchase_date = models.DateTimeField('Purchase Date', )
    improvements = models.CharField('Land Improvements', max_length=100, default='nil')
    encumbrances = models.CharField('Encumbrances', max_length=100, default='nil')
    registered = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "%s" % self.parcel.lr_no

    class Meta:
        # Gives the proper plural name for admin
        db_table = 'parcel_details'
        verbose_name_plural = "parcel_details"


class Centroids(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)
    perimeter = models.FloatField()
    area_ha = models.FloatField()
    lr_no = models.CharField(max_length=10)
    geom = models.MultiPointField(srid=4326)

    class Meta:
        db_table = 'centroids'
        verbose_name_plural = "centroid"

    def __str__(self):
        return self.lr_no
