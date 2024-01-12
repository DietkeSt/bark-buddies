# reviews/forms.py
from .models import Comment
from booking.models import Service
from django import forms


class CommentForm(forms.ModelForm):
    """
    Form for Comment model with custom field settings.
    """

    class Meta:
        """
        Meta options for CommentForm.
        """
        model = Comment
        fields = ('service', 'body',)

    def __init__(self, *args, **kwargs):
        """
        Init method to set 'service' field queryset.
        """
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(status=1)
