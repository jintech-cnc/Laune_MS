from django.urls import path
from . import views

urlpatterns = [
    path('', views.devis_request, name='devis_request'),
    path('confirmation/', views.devis_success, name='devis_success'),
]
