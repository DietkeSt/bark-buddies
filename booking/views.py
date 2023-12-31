import json
from datetime import datetime, timedelta
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from .models import Service, Booking, Availability
from .forms import BookingForm, EditBookingForm
from reviews.forms import CommentForm
from django.utils import timezone
from reviews.models import Comment


class GetUnavailableTimes(View):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        unavailable_times = []

        if start_date and end_date:
            start_date_obj = datetime.strptime(
                start_date,
                '%Y-%m-%d'
            ).date()
            end_date_obj = datetime.strptime(
                end_date,
                '%Y-%m-%d'
            ).date()

            bookings = Booking.objects.filter(
                start_date__lte=end_date_obj,
                end_date__gte=start_date_obj,
                is_cancelled=False
            )

            for booking in bookings:
                if booking.time:
                    unavailable_times.append(
                        booking.time.time.strftime('%H:%M'))

        return JsonResponse(
            {'unavailable_times': list(set(unavailable_times))}
        )


class ServiceDetail(View):

    def get(self, request, slug, *args, **kwargs):
        service = get_object_or_404(Service, slug=slug)
        comments = service.comments.filter(approved=True)
        has_comments = comments.filter(approved=True).exists()
        today = timezone.now().date()
        unavailable_dates = Availability.objects.filter(
            unavailable_to__gte=today
        )
        other_services = Service.objects.filter(status=1).exclude(slug=slug)

        return render(request, "service_detail.html", {
            "service": service,
            "comments": comments,
            "has_comments": has_comments,
            "booking_form": BookingForm(),
            "unavailable_dates": unavailable_dates,
            "other_services": other_services,
        })


class BookServiceView(LoginRequiredMixin, View):
    def post(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking_start = booking.start_date
            booking_end = booking.end_date

            # Handle 'just_one_day' field
            if form.cleaned_data.get('just_one_day'):
                booking.end_date = booking.start_date

            # Validate the booking date to be at least 24 hours in the future
            if timezone.now() + timedelta(days=1) > timezone.make_aware(datetime.combine(booking_start, datetime.min.time())):
                messages.error(request, 'You must book at least 24 hours in advance.')
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            # Check for availability and overlapping bookings
            if not Booking.is_period_available(
                booking_start,
                booking_end
            ):
                messages.error(request, 'Selected dates are unavailable.')
                return HttpResponseRedirect(
                    reverse('service_detail', args=[service.slug])
                )

            if Booking.has_overlapping_bookings(
                booking_start,
                booking_end,
                booking.time
            ):
                messages.error(request, 'Selected time is already booked.')
                return HttpResponseRedirect(
                    reverse('service_detail', args=[service.slug])
                )

            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking successful.')
            return HttpResponseRedirect(reverse('view_bookings'))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return HttpResponseRedirect(
                reverse('service_detail', args=[service.slug])
            )


class BookingsView(LoginRequiredMixin, View):
    def get(self, request):
        bookings = Booking.get_future_bookings_for_user(request.user)
        comment_form = CommentForm()
        user_has_bookings = Booking.objects.filter(user=request.user, end_date__lt=timezone.now(), is_cancelled=False).exists()

        return render(request, 'view_bookings.html', {
            'bookings': bookings,
            'comment_form': comment_form,
            'user_has_bookings': user_has_bookings,
        })

    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            Comment.create_comment(request.user, comment_form.cleaned_data)
            messages.success(
                request, 'Thanks! Your comment is now being reviewed.'
                )
        else:
            messages.error(request, "There was an error with your submission.")
        return redirect('view_bookings')


class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        if booking.cancel_booking():
            messages.success(request, "Booking cancelled successfully.")
        else:
            messages.error(
                request,
                "Cancellation not allowed less than 24 hours in advance."
            )
        return redirect('view_bookings')


class DeleteBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(
            Booking, id=booking_id, user=request.user, is_cancelled=True
        )
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('view_bookings')


class EditBookingView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        form = EditBookingForm(instance=booking)
        return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully.')
            return HttpResponseRedirect(reverse('view_bookings'))
        else:
            return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.name = request.user.username
            comment.email = request.user.email
            comment.save()
            return redirect('view_bookings')
        return redirect('view_bookings')
