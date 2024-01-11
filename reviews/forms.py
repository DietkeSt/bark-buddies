# models/forms.py
from .models import Comment
from booking.models import Service
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'service',
            'body',
        )

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # Set 'service' field to only include published services
        self.fields['service'].queryset = Service.objects.filter(status=1)
