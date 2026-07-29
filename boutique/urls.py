from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogue_list, name='catalogue_list'),
    path('<slug:slug>/', views.catalogue_detail, name='catalogue_detail'),
]
