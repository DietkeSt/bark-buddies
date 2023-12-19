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


class BookServiceView(LoginRequiredMixin, View):
    @staticmethod
    def has_overlapping_bookings(start_date, end_date, time):
        overlapping_bookings = Booking.objects.filter(
            start_date=start_date,
            end_date=end_date,
            time=time,
            is_cancelled=False
        )
        return overlapping_bookings.exists()

    def post(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
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
                    f"{period.unavailable_from.strftime('%d/%m/%Y')} to {period.unavailable_to.strftime('%d/%m/%Y')}"
                    for period in unavailable_periods
                ])
                messages.error(
                    request,
                    f'Dates {unavailable_str} are unavailable for booking.'
                )
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            # Check for overlapping bookings
            if BookServiceView.has_overlapping_bookings(booking.start_date, booking.end_date, booking.time):
                messages.error(
                    request,
                    'The selected time is already booked for those dates.'
                )
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))

            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking successful.')
            return HttpResponseRedirect(reverse('view_bookings'))

        return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))


class BookingsView(LoginRequiredMixin, View):
    def get(self, request):
        # Get current date
        current_date = timezone.now().date()

        # Booking filter to only show future bookings
        bookings = Booking.objects.filter(
            user=request.user, 
            start_date__gte=current_date, 
        ).order_by('start_date')

        comments = Comment.objects.filter(name=request.user.username, approved=True)
        comment_form = CommentForm()
        commented = Comment.objects.filter(name=request.user.username, approved=False).exists()

        return render(request, 'view_bookings.html', {
            'bookings': bookings,
            'comments': comments,
            'comment_form': comment_form,
            'commented': commented
        })

    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.name = request.user.username
            comment.save()
            messages.success(request, 'Review added successfully.')
            return redirect('view_bookings')
        else:
            # Handle not valid form
            bookings = Booking.objects.filter(user=request.user).order_by('start_date')
            comments = Comment.objects.filter(name=request.user.username, approved=True)
            commented = Comment.objects.filter(name=request.user.username, approved=False).exists()
            return render(request, 'view_bookings.html', {
                'bookings': bookings,
                'comments': comments,
                'comment_form': comment_form,
                'commented': commented
            })



class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        if booking.can_cancel():
            booking.cancel()
            messages.success(request, "Booking cancelled successfully.")
        else:
            messages.error(request, "Cancellation not allowed less than 24 hours in advance.")
        return redirect('view_bookings')


class DeleteBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user, is_cancelled=True)
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
