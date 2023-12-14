import datetime
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.conf import settings
from django import forms
from django.utils import timezone

STATUS = (
    (0, "Draft"),
    (1, "Published"),
)


class Service(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.DurationField(default=datetime.timedelta(hours=1))
    featured_image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Comment(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class TimeSlot(models.Model):
    time_of_day = models.CharField(max_length=10, choices=[(
        'Morning', 'Morning'), ('Noon', 'Noon'), ('Evening', 'Evening')])
    limit = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.time_of_day} (Limit: {self.limit})"
        

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} booked {self.service} from {self.start_date} to {self.end_date} at {self.time_slot}'

    # Add a method to check if the booking can be cancelled
    def can_cancel(self):
        return timezone.now() <= timezone.make_aware(datetime.datetime.combine(self.start_date, datetime.time.min)) - datetime.timedelta(days=1)

    def cancel(self):
        self.is_cancelled = True
        self.save()
