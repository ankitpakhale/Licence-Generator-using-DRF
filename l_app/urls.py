from django.urls import path
from.views import exportcsv
from . import views

urlpatterns = [
    path('create_seller/', views.create_seller.as_view(), name='create_seller'),
    path('all/', views.All_create_seller.as_view(), name='All_create_seller'),
    path('', views.generate_licence.as_view(), name='generate_licence'),
    path('export/', exportcsv, name='exportcsv'),
]