from django import forms
from .models import Booking
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "date", "start_time", "end_time"]
    
    def clean(self): # Nettoyage
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time') # None -> False | True
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("L'heure de début doit etre avant l'heure de fin")

        if room and date and start_time and end_time:
            conflicts = Booking.objects.filter(
                room=room,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if conflicts.exists() or len(conflicts) != 0:
                raise ValidationError("Conflit: Cette salle est déjà réservée à ce créneau.")
        
        return cleaned_data