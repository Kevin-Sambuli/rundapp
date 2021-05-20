from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


#
# urlpatterns = [
#     path('ownership/', views.ownership, name='login'),
# ]

from django.urls import path
from .views import EmailAttachementView, ownership_view, my_property

urlpatterns = [
    path('email/', EmailAttachementView.as_view(), name='emailattachment'),
    path('search/', views.search, name='search'),
    path('my_property/', my_property, name='myproperty'),
    path('ownership/', ownership_view, name='own'),
    path('my_parcels_map/', TemplateView.as_view(template_name='ownership/parcel_map.html'), name='my_parcel_map'),
    path('parcel_search/', TemplateView.as_view(template_name='ownership/parcel_search.html'), name='parcel_search'),

    ]