from django.shortcuts import render, redirect
from reservation.models import *
from django.db.models import Q
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from reservation.forms import FilterForm
from django.contrib.auth import login


class RoomsList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'reservation/rooms_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_order = self.request.GET.get('filter', 'increase')  # Получаем значение фильтра из GET-параметров

        if filter_order == 'increase':
            queryset = Room.objects.all().order_by('number')
        elif filter_order == 'decrease':
            queryset = Room.objects.all().order_by('-number')
        else:
            queryset = Room.objects.all()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context

def booking_details(request, pk):
    booking = Booking.objects.get(id=pk)

    return render(request, "reservation/booking_details.html", context={"booking":booking})

def room_details(request, pk):
    room = Room.objects.get(id=pk)

    return render(request, "reservation/room_details.html", context={"room":room})

def book_room(request):
    if not request.user.is_authenticated:
        return redirect('reservation:login')
    if request.method == 'POST':
        room = request.POST.get('room-number')
        start_time_str = str(request.POST.get('start-time')) 
        end_time_str = str(request.POST.get('end-time'))  


        start_time = start_time_str.replace('T', ' ')
        end_time = end_time_str.replace('T', ' ')

        try:
            room = Room.objects.get(number=room)
        except Room.DoesNotExist:
            return render(request, 'reservation/booking_form.html', {'message': 'Цієї кімнати не існує'})
        except ValueError:
            return render(request, 'reservation/booking_form.html', {'message': "Неправильний номер кімнати"})

        bookings = Booking.objects.filter(
            Q(start_time__lt=end_time) & Q(end_time__gt=start_time),
            room=room,
        )

        if bookings.exists():
            return render(request, 'reservation/booking_form.html', {'message': 'Кімната вже заброньована на цей час'})

        booking = Booking.objects.create(
            user=request.user,
            room=room,
            start_time=start_time,
            end_time=end_time
        )

        return redirect('reservation:booking-details', pk=booking.id)


    else:
        return render(request, "reservation/booking_form.html")
    

class CustomLoginView(LoginView):
    template_name = "reservation/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("reservation:home")

class CustomLogoutView(LogoutView):
    next_page = "reservation:login"

class RegisterView(CreateView):
    template_name = "reservation/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("reservation:login"))