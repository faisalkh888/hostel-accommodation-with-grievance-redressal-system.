from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Grievance

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['subject', 'description']
