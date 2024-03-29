# booking/models.py
from datetime import timedelta
import datetime
from decimal import Decimal
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.utils import timezone
from django.utils.text import slugify


STATUS = (
    (0, "Draft"),
    (1, "Published"),
)


class ServiceManager(models.Manager):
    """ Custom manager for Service model. """
    def active_services(self):
        """ Return active services. """
        return self.get_queryset().filter(status=1)


class Service(models.Model):
    """ Represents a service in the booking system. """
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
        """ Return active services sorted by title. """
        return cls.objects.filter(
            status=1
        ).order_by('title')

    @classmethod
    def get_service_with_comments(cls, slug):
        from reviews.models import Comment
        service = cls.objects.filter(
            slug=slug, status=1
        ).first()
        if service:
            comments = Comment.objects.filter(
                service=service, approved=True
            ).order_by('created_on')
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
    """ Represents a specific time for bookings. """
    time = models.TimeField(
        default=datetime.time(8, 0)
    )

    def __str__(self):
        return f"{self.time.strftime('%H:%M')}"


class Availability(models.Model):
    """ Represents unavailable dates for booking. """
    unavailable_from = models.DateField()
    unavailable_to = models.DateField()

    def __str__(self):
        return (
            f"Unavailable from {self.unavailable_from} "
            f"to {self.unavailable_to}"
        )


class Booking(models.Model):
    """ Represents a booking made by a user. """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.ForeignKey(
        BookingTime,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    comments = models.TextField(
        blank=True,
        null=True,
        max_length=400
    )
    is_cancelled = models.BooleanField(
        default=False
    )
    add_second_dog = models.BooleanField(
        default=False
    )
    additional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
        )

    def save(self, *args, **kwargs):
        """ Save method with custom price calculation. """
        # Calculate the number of days for the booking
        booking_duration = (self.end_date - self.start_date).days + 1

        # Calculate total price based on the number of days
        total_price = self.service.price * booking_duration

        # If 'add_second_dog' is true, add 50% of the total price
        if self.add_second_dog:
            self.additional_price = total_price * Decimal('0.5')
        else:
            self.additional_price = Decimal('0.00')

        super(Booking, self).save(*args, **kwargs)

    def total_price(self):
        # Calculate the total price including any additional charges
        booking_duration = (self.end_date - self.start_date).days + 1
        return (self.service.price * booking_duration) + self.additional_price

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
        return (
            f"{self.user} booked {self.service} from {self.start_date} "
            f"to {self.end_date} at {time_str}"
        )

    @staticmethod
    def has_overlapping_bookings(
        start_date,
        end_date,
        time,
        exclude_booking_id=None
    ):
        query = Booking.objects.filter(
            start_date=start_date,
            end_date=end_date,
            time=time,
            is_cancelled=False
        )
        if exclude_booking_id:
            query = query.exclude(id=exclude_booking_id)
        return query.exists()

    @staticmethod
    def is_period_available(
        start_date,
        end_date
    ):
        return not Availability.objects.filter(
            unavailable_from__lte=end_date,
            unavailable_to__gte=start_date
        ).exists()

    def can_cancel(self):
        current_date = timezone.now().date()  # Convert to date
        return current_date < self.start_date - timedelta(hours=24)

    @classmethod
    def get_future_bookings_for_user(cls, user):
        """ Return future bookings for a given user. """
        current_date = timezone.now().date()
        return cls.objects.filter(
            user=user,
            start_date__gte=current_date
        ).order_by('start_date', 'time')
