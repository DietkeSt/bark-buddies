import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.conf import settings
from django import forms
from django.utils import timezone
from django.utils.text import slugify

STATUS = (
    (0, "Draft"),
    (1, "Published"),
)


class Service(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.DurationField(default=datetime.timedelta(hours=1))
    featured_image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=0)

    @classmethod
    def get_active_services(cls):
        return cls.objects.filter(status=1).order_by('title')

    @classmethod
    def get_service_with_comments(cls, slug):
        service = cls.objects.filter(slug=slug, status=1).first()
        if service:
            comments = service.comments.filter(
                approved=True).order_by('created_on')
            return service, comments
        return None, None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Availability(models.Model):
    unavailable_from = models.DateField()
    unavailable_to = models.DateField()

    def __str__(self):
        return f"Unavailable from {self.unavailable_from} to {self.unavailable_to}"


class Comment(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    @classmethod
    def create_comment(cls, user, form_data):
        comment = cls(name=user.username, email=user.email, **form_data)
        comment.save()
        return comment
   

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField(default=datetime.time(8, 0))
    comments = models.TextField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} booked {self.service} from {self.start_date} to {self.end_date} at {self.time.strftime("%I:%M %p")}'

    @staticmethod
    def has_overlapping_bookings(start_date, end_date, time):
        return Booking.objects.filter(start_date=start_date, end_date=end_date, time=time, is_cancelled=False).exists()

    @staticmethod
    def is_period_available(start_date, end_date):
        return not Availability.objects.filter(unavailable_from__lt=end_date, unavailable_to__gt=start_date).exists()

    def can_cancel(self):
        current_date = timezone.now().date()  # Convert to date
        return current_date < self.start_date - timedelta(hours=24)

    def cancel_booking(self):
        if self.can_cancel():
            self.is_cancelled = True
            self.save()
            return True
        return False

    @classmethod
    def get_future_bookings_for_user(cls, user):
        current_date = timezone.now().date()
        return cls.objects.filter(user=user, start_date__gte=current_date).order_by('start_date')
