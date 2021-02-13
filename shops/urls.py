from django.urls import path
from .views import CitySet, StreetSet, ShopSet

urlpatterns = [
    path(
        'city/',
        view=CitySet.as_view(),
        name='city'
    ),
    path(
        'city/street/',
        view=StreetSet.as_view(
            actions={
                'get': 'list',
            }
        ),
        name='street'
    ),
    path(
        'shop',
        view=ShopSet.as_view(
            actions={
                'post': 'create',
                'get': 'list'
            }
        ),
        name='street'
    ),
]
