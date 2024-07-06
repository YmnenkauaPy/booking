from django.shortcuts import render, redirect
from reservation.models import *
from django.http import HttpResponse


def rooms_list(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}

    return render(request=request, template_name = 'reservation/rooms_list.html', context=context)

def booking_details(request, pk):
    booking = Booking.objects.get(id=pk)

    return render(request, "reservation/booking_details.html", context={"booking":booking})

def room_details(request, pk):
    room = Room.objects.get(id=pk)

    return render(request, "reservation/room_details.html", context={"room":room})

def book_room(request):
    if request.method == 'POST':
        room_number = request.POST.get("room-number")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            room = Room.objects.get(number=room_number)
        except ValueError:
            return HttpResponse('Wrong room number', status=400)
        except Room.DoesNotExist:
            return HttpResponse('Room does not exist', status=404)
        
        booking = Booking.objects.create(user=request.user, room=room, start_time=start_time, end_time=end_time)

        return redirect("booking-details", pk=booking.id)


    else:
        return render(request, "reservation/booking_form.html")