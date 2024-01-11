from .models import Booking, BookingTime
from reviews.models import Comment
from django import forms


class BookingForm(forms.ModelForm):
    add_second_dog = forms.BooleanField(
        required=False,
        label='Add Second Dog*'
    )
    just_one_day = forms.BooleanField(
        required=False, 
        label='One Day'
    )
    time = forms.ModelChoiceField(
        queryset=BookingTime.objects.all(),
        to_field_name="time",
        required=True,
        widget=forms.Select(),
        empty_label=None
    )

    class Meta:
        model = Booking
        fields = [
            'start_date',
            'just_one_day',
            'end_date',
            'time',
            'comments',
            'add_second_dog',
        ]
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
                ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
                ),
        }

    def clean(self):
        cleaned_data = super().clean()
        just_one_day = cleaned_data.get(
            'just_one_day'
        )
        start_date = cleaned_data.get(
            'start_date'
        )

        if just_one_day and start_date:
            cleaned_data['end_date'] = start_date

        return cleaned_data


class EditBookingForm(forms.ModelForm):
    add_second_dog = forms.BooleanField(
        required=False, 
        label='Add Second Dog*'
        )
    just_one_day = forms.BooleanField(
        required=False, 
        label='One Day'
        )
    time = forms.ModelChoiceField(
        queryset=BookingTime.objects.all(),
        to_field_name="time",
        required=True,
        widget=forms.Select(),
        empty_label=None
    )

    class Meta:
        model = Booking
        fields = [
            'start_date', 
            'just_one_day', 
            'end_date', 
            'time', 
            'comments', 
            'add_second_dog'
        ]
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        just_one_day = cleaned_data.get('just_one_day')
        start_date = cleaned_data.get('start_date')

        if just_one_day and start_date:
            cleaned_data['end_date'] = start_date

        return cleaned_data
