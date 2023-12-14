from .models import Comment, Booking
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('service', 'body',)


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        available_slots = kwargs.pop('available_slots', [])
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['time_slot'].choices = available_slots

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'time_slot', 'comments']
