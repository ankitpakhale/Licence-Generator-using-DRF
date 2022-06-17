from django.urls import path
from .views import *

urlpatterns = [
    path('create_seller/', create_seller, name='create_seller'),
    path('', generate_licence, name='generate_licence'),
    path('export/', exportcsv, name='exportcsv'),
]