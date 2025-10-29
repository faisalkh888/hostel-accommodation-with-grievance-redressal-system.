from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, BookingForm, GrievanceForm
from .models import Room, Booking, Grievance
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        grievances = Grievance.objects.all().order_by('-created_at')
        rooms = Room.objects.all()
        bookings = Booking.objects.all()
        return render(request, 'dashboard.html', {'grievances': grievances, 'rooms': rooms, 'bookings': bookings})
    else:
        bookings = Booking.objects.filter(student=request.user)
        grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
        return render(request, 'dashboard.html', {'bookings': bookings, 'grievances': grievances})
    
@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def rooms(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'rooms.html', {'rooms': rooms})

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.room = room
            booking.save()
            room.is_available = False
            room.save()
            return redirect('dashboard')
    else:
        form = BookingForm()
    return render(request, 'room_detail.html', {'room': room, 'form': form})

@login_required
def grievances(request):
    if request.user.is_staff:
        grievances = Grievance.objects.all().order_by('-created_at')
    else:
        grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'grievances.html', {'grievances': grievances})

@login_required
def create_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.student = request.user
            grievance.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'grievance_id': grievance.id})
            return redirect('grievances')
    else:
        form = GrievanceForm()
    return render(request, 'grievance_create.html', {'form': form})

@login_required
def get_grievance_status(request, grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id)
    return JsonResponse({'status': grievance.status})

@login_required
def update_grievance_status(request, grievance_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            grievance = get_object_or_404(Grievance, id=grievance_id)
            
            if new_status in [choice[0] for choice in Grievance.STATUS_CHOICES]:
                grievance.status = new_status
                grievance.save()
                return JsonResponse({'status': 'success', 'message': 'Status updated.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid status.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
