import datetime
import logging
import json
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic, View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Service, Booking, Comment, Availability, BookingTime
from .forms import CommentForm, BookingForm
from django.utils import timezone


class ServiceList(generic.ListView):
    model = Service
    queryset = Service.get_active_services()
    template_name = 'index.html'


class GetUnavailableTimes(View):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        unavailable_times = []

        if start_date and end_date:
            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            bookings = Booking.objects.filter(
                start_date__lte=end_date_obj,
                end_date__gte=start_date_obj,
                is_cancelled=False
            )

            for booking in bookings:
                if booking.time:
                    unavailable_times.append(
                        booking.time.time.strftime('%H:%M'))

        return JsonResponse({'unavailable_times': list(set(unavailable_times))})


class ServiceDetail(View):

    def get(self, request, slug, *args, **kwargs):
        service, comments = Service.get_service_with_comments(slug)
        unavailable_dates = Availability.objects.all()

        if not service:
            return redirect('error_404')

        return render(request, "service_detail.html", {
            "service": service,
            "comments": comments,
            "commented": False,
            "comment_form": CommentForm(),
            "booking_form": BookingForm(),
            "unavailable_dates": unavailable_dates,
        })

    def post(self, request, slug, *args, **kwargs):
        queryset = Service.objects.filter(status=1)
        service = get_object_or_404(queryset, slug=slug)
        comments = service.comments.filter(
            approved=True).order_by('created_on')

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.service = service
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "service_detail.html",
            {
                "service": service,
                "comments": comments,
                "commented": True,
                "comment_form": CommentForm()
            },
        )


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

            # Check for availability and overlapping bookings
            if not Booking.is_period_available(booking_start, booking_end):
                messages.error(request, 'Selected dates are unavailable.')
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            if Booking.has_overlapping_bookings(booking_start, booking_end, booking.time):
                messages.error(request, 'Selected time is already booked.')
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking successful.')
            return HttpResponseRedirect(reverse('view_bookings'))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))


class BookingsView(LoginRequiredMixin, View):
    def get(self, request):
        bookings = Booking.get_future_bookings_for_user(request.user)
        comments = Comment.objects.filter(
            name=request.user.username, approved=True)
        comment_form = CommentForm()
        commented = Comment.objects.filter(
            name=request.user.username, approved=False).exists()

        return render(request, 'view_bookings.html', {
            'bookings': bookings,
            'comments': comments,
            'comment_form': comment_form,
            'commented': commented
        })

    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            Comment.create_comment(request.user, comment_form.cleaned_data)
            messages.success(request, 'Review added successfully.')
            return redirect('view_bookings')
        else:
            return self.get(request)


class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        if booking.cancel_booking():
            messages.success(request, "Booking cancelled successfully.")
        else:
            messages.error(
                request, "Cancellation not allowed less than 24 hours in advance.")
        return redirect('view_bookings')


class DeleteBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(
            Booking, id=booking_id, user=request.user, is_cancelled=True)
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('view_bookings')
        

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
