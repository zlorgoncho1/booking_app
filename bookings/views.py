from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import BookingForm

# Create your views here.
@login_required
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            # return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})