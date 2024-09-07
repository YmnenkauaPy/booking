from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    FILTER_CHOICES = [
        ('increase', "За зростанням"),
        ('decrease', "За спаданням"),
    ]

    number = models.IntegerField()
    filter = models.CharField(max_length=23, choices=FILTER_CHOICES, default='increase')
    capacity = models.IntegerField()
    location = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f'{self.number}'

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="booking")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.room} booked - by {self.user}"

