from django.db import models
import datetime
from django.conf import settings


# Create your models here.
class Transfer(models.Model):
    seller_email = models.EmailField(verbose_name="seller's email", blank=False, null=False, max_length=100)
    buyer_email = models.EmailField(verbose_name="Buyer's email", blank=False, null=False, max_length=100)
    parcel_no = models.IntegerField(blank=False, null=False, verbose_name="Parcel No") #max_length=3,
    amount = models.IntegerField(blank=False, null=False, verbose_name="Amount")
    file_upload = models.FileField(upload_to='documents/')
    transfer_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transfers'
        verbose_name_plural = "transfers"

    def __str__(self):
        return self.seller_email


class Subdivision(models.Model):
    email = models.EmailField(verbose_name="Email", blank=False, null=False, max_length=100, default=None)
    parcel_no = models.CharField(max_length=10, blank=False, null=False)
    reason = models.TextField(max_length=200, blank=False, null=False)
    subdivision_date = models.DateTimeField()

    class Meta:
        db_table = 'subdivisions'
        verbose_name_plural = "subdivisions"

    def __str__(self):
        return self.email
