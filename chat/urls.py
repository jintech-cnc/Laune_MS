from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='chat_send'),
    path('history/', views.get_history, name='chat_history'),
    path('admin-view/', views.chat_admin_view, name='chat_admin_view'),
]
