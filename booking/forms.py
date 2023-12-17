from .models import Comment, Booking
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('service', 'body',)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'time', 'comments']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
