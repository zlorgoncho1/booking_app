from django.db import models
from rooms.models import Room
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.room.name} - {self.date} {self.start_time}-{self.end_time}"
    
    class Meta:
        unique_together = ('room', 'date', 'start_time', 'end_time')