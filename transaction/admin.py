from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from transaction.models import Transfer, Subdivision


class TransferAdmin(admin.ModelAdmin):
    list_display = ('seller_email', 'buyer_email', 'parcel_no', 'file_upload')
    search_fields = ('parcel_no', 'seller_email')
    readonly_fields = ('parcel_no',)
    list_display_links = ('seller_email',)
    filter_horizontal = ()
    list_per_page = 10  # record 10 per page
    # list_filter = ('is_staff', 'is_admin', 'is_superuser', 'is_active')
    fieldsets = ()


class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('email', 'parcel_no', 'reason')
    search_fields = ('parcel_no', 'email')
    readonly_fields = ('reason','parcel_no')
    list_display_links = ('email',)
    filter_horizontal = ()
    list_per_page = 10  # record 10 per page
    fieldsets = ()


# Register your models here.
admin.site.register(Transfer, TransferAdmin)
admin.site.register(Subdivision, SubdivisionAdmin)

