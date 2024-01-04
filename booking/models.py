import datetime
from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.db.models import Q, F, CheckConstraint
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.utils.text import slugify


STATUS = (
    (0, "Draft"),
    (1, "Published"),
)


class ServiceManager(models.Manager):
    def active_services(self):
        return self.get_queryset().filter(status=1)


class Service(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.DurationField(default=datetime.timedelta(hours=1))
    featured_image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=0)

    # Custom manager
    objects = models.Manager()
    active = ServiceManager()

    @classmethod
    def get_active_services(cls):
        return cls.objects.filter(status=1).order_by('title')

    @classmethod
    def get_service_with_comments(cls, slug):
        from reviews.models import Comment
        service = cls.objects.filter(slug=slug, status=1).first()
        if service:
            comments = Comment.objects.filter(
                service=service, approved=True).order_by('created_on')
            return service, comments
        return None, None

    def publish(self):
        self.status = 1
        self.save()

    def unpublish(self):
        self.status = 0
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookingTime(models.Model):
    time = models.TimeField(default=datetime.time(8, 0))

    def __str__(self):
        return f"{self.time.strftime('%H:%M')}"


class Availability(models.Model):
    unavailable_from = models.DateField()
    unavailable_to = models.DateField()

    def __str__(self):
        return (f"Unavailable from {self.unavailable_from} "
                f"to {self.unavailable_to}")


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.ForeignKey(
        BookingTime, on_delete=models.SET_NULL, blank=True, null=True
        )
    comments = models.TextField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    add_second_dog = models.BooleanField(default=False)
    additional_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
        )

    def save(self, *args, **kwargs):
        if self.add_second_dog:
            self.additional_price = self.service.price * Decimal('0.5')
        super().save(*args, **kwargs)

    def total_price(self):
        return self.service.price + self.additional_price

    # Check if end date is greater than or equal to start date
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(end_date__gte=F('start_date')),
                name='end_date_gte_start_date'
            )
        ]

    def cancel_booking(self):
        if self.can_cancel():
            self.is_cancelled = True
            self.save()
            return True
        return False

    def delete_booking(self):
        if not self.is_cancelled:
            return False
        self.delete()
        return True

    def __str__(self):
        time_str = self.time.time.strftime(
            "%I:%M %p") if self.time else "No time set"
        return (f"{self.user} booked {self.service} from {self.start_date} "
                f"to {self.end_date} at {time_str}")

    @staticmethod
    def has_overlapping_bookings(start_date, end_date, time):
        return Booking.objects.filter(
            start_date=start_date,
            end_date=end_date,
            time=time,
            is_cancelled=False
        ).exists()

    @staticmethod
    def is_period_available(start_date, end_date):
        return not Availability.objects.filter(
            unavailable_from__lt=end_date,
            unavailable_to__gt=start_date
        ).exists()

    def can_cancel(self):
        current_date = timezone.now().date()  # Convert to date
        return current_date < self.start_date - timedelta(hours=24)

    @classmethod
    def get_future_bookings_for_user(cls, user):
        current_date = timezone.now().date()
        return cls.objects.filter(
            user=user,
            start_date__gte=current_date
        ).order_by('start_date', 'time')
