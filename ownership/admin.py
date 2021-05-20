from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ownership


class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'parcel')
    search_fields = ('owner', 'parcel')
    list_display_links = ('owner',)


# Register your models here.
admin.site.register(Ownership, OwnershipAdmin)
