from .models import Comment, Booking
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('service', 'body',)


class BookingForm(forms.ModelForm):
    just_one_day = forms.BooleanField(required=False, label='Just one day')

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'time', 'comments']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        just_one_day = cleaned_data.get('just_one_day')
        start_date = cleaned_data.get('start_date')

        if just_one_day and start_date:
            cleaned_data['end_date'] = start_date

        return cleaned_data
