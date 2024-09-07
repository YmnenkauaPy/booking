from django.urls import path
from .views import *

urlpatterns = [
    path('', RoomsList.as_view(), name = 'home'),
    path('booking_details/<int:pk>/', booking_details, name = 'booking-details'),
    path('book-room', book_room, name = 'book-room'),
    path('room_details/<int:pk>/', room_details, name = 'room-detail'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]

app_name = "reservation"