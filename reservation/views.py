from django.shortcuts import render
from reservation.models import *

def rooms_list(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}

    return render(request=request, template_name = 'reservation/room_list.html', context=context)