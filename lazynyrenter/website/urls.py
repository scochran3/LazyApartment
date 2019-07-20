from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('by-neighborhood', views.byNeighborhood, name='byNeighborhood'),
    path('by-zip-code', views.byZipCode, name='byZipCode'),
    path('by-borough', views.byBorough, name='byBorough'),
    path('new-york-city-apartment-prices-by-neighborhood/<neighborhood>/', views.neighborhoodData, name='neighborhoodData'),
    path('new-york-city-apartment-prices-by-zip-code/<zipCode>/', views.zipCodeData, name='zipCodeData'),
    path('new-york-city-apartment-prices-by-borough/<borough>/', views.boroughData, name='boroughData'),

]