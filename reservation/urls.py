from django.urls import path
from .views import *

urlpatterns = [
    path('', rooms_list, name = 'home'),
    path('booking_details/<int:pk>/', booking_details, name = 'booking-details'),
    path('book-room', book_room, name = 'book-room'),
    path('room_details/<int:pk>/', room_details, name = 'room-details'),
]