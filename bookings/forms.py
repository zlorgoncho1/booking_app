from django import forms
from .models import Booking
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "date", "start_time", "end_time"]
        labels = {
            "room": "Salle",
            "date": "Date",
            "start_time": "Heure de début",
            "end_time": "Heure de fin"
        }
        help_texts = {
            "room": "Sélectionnez la salle à réserver",
            "date": "Sélectionnez la date de la réservation",
            "start_time": "Sélectionnez l'heure de début de la réservation",
            "end_time": "Sélectionnez l'heure de fin de la réservation"
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }
        error_messages = {
            "date": {
                "invalid": "Date invalide"
            }
        }        
            
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