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
from .models import Service, Booking, Comment, Availability
from .forms import CommentForm, BookingForm
from django.utils import timezone


class ServiceList(generic.ListView):
    model = Service
    queryset = Service.objects.filter(status=1).order_by('title')
    template_name = 'index.html'


class ServiceDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Service.objects.filter(status=1)
        service = get_object_or_404(queryset, slug=slug)
        comments = service.comments.filter(
            approved=True).order_by('created_on')

        booking_form = BookingForm()

        return render(
            request,
            "service_detail.html",
            {
                "service": service,
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm(),
                "booking_form": booking_form,
            },
        )

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


class BookingView(View):
    template_name = 'booking_page.html'

    def get(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        form = BookingForm(available_slots=get_available_slots())
        return render(request, self.template_name, {'form': form, 'service': service})

    def post(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        form = BookingForm(request.POST, available_slots=get_available_slots())

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking successful.')
            return redirect('view_bookings')  # Redirect to the view bookings page

        messages.error(request, 'There was an error with your booking.')
        return render(request, self.template_name, {'form': form, 'service': service})


# Check for overlapping bookings
def has_overlapping_bookings(start_date, end_date, time):
    overlapping_bookings = Booking.objects.filter(
        start_date=start_date,
        end_date=end_date,
        time=time,
        is_cancelled=False
    )

    return overlapping_bookings.exists()


@login_required
def book_service(request, service_id):
    service = Service.objects.get(id=service_id)
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking_start = booking.start_date
            booking_end = booking.end_date

            # Check for unavailable periods
            unavailable_periods = Availability.objects.filter(
                unavailable_from__lt=booking_end,
                unavailable_to__gt=booking_start
            )

            if unavailable_periods.exists():
                unavailable_str = ", ".join([
                    f"{period.unavailable_from} to {period.unavailable_to}"
                    for period in unavailable_periods
                ])
                messages.error(
                    request,
                    f'Selected dates are within an unavailable period: {unavailable_str}.'
                )
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            # Check for overlapping bookings
            if has_overlapping_bookings(booking.start_date, booking.end_date, booking.time):
                messages.error(
                    request,
                    f'The selected time slot is already booked for that day.'
                )
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking successful.')
            return HttpResponseRedirect(reverse('view_bookings'))

    return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))


@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('start_date')
    user_comments = Comment.objects.filter(
        name=request.user.username)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.name = request.user.username
            comment.email = request.user.email
            comment.save()
            messages.success(request, 'Review added successfully.')
            return redirect('view_bookings')
    else:
        comment_form = CommentForm()

    return render(request, 'view_bookings.html', {
        'bookings': bookings,
        'comments': user_comments,
        'comment_form': comment_form
    })


@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    if booking.can_cancel():
        booking.cancel()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(
            request, "Cancellation is not allowed less than 24 hours in advance.")
    
    return redirect('view_bookings')


@login_required
def add_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.name = request.user.username
            comment.email = request.user.email
            comment.save()
            return redirect('view_bookings')
    else:
        return redirect('view_bookings')
