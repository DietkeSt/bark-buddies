import datetime
import logging
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic, View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Service, Booking, TimeSlot, Comment
from .forms import CommentForm, BookingForm
from django.utils import timezone


class ServiceList(generic.ListView):
    model = Service
    queryset = Service.objects.filter(status=1).order_by('title')
    template_name = 'index.html'


def get_available_slots():
    today = timezone.now().date()
    slots = TimeSlot.objects.all()
    available_slots = []

    for slot in slots:
        # Check for bookings that overlap with 'today'
        overlapping_bookings = Booking.objects.filter(
            time_slot=slot,
            start_date__lte=today,
            end_date__gte=today   
        ).count()

        if overlapping_bookings < slot.limit:
            available_slots.append(
                (slot.id, f"{slot.time_of_day} (Available)"))
        else:
            available_slots.append((slot.id, f"{slot.time_of_day} (Full)"))

    return available_slots


def get_time_slots(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    today = timezone.now().date()

    slots = TimeSlot.objects.all()
    slots_data = []

    for slot in slots:
        overlapping_bookings = Booking.objects.filter(
            time_slot=slot,
            start_date__lte=start_date,
            end_date__gte=end_date
        ).count()

        slot_data = {
            'id': slot.id,
            'display': f"{slot.time_of_day}",
            'full': overlapping_bookings >= slot.limit
        }
        slots_data.append(slot_data)

    return JsonResponse({'slots': slots_data})


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
                "booking_form": booking_form
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


@login_required
def book_service(request, service_id):
    service = Service.objects.get(id=service_id)
    form = BookingForm(available_slots=get_available_slots())

    if request.method == 'POST':
        form = BookingForm(request.POST, available_slots=get_available_slots())
        if form.is_valid():
            booking = form.save(commit=False)
            selected_slot = TimeSlot.objects.get(id=booking.time_slot.id)

            if Booking.objects.filter(time_slot=selected_slot, start_date=booking.start_date).count() >= selected_slot.limit:
                messages.error(
                    request, 'Selected time slot is full. Please choose another time.')
                return HttpResponseRedirect(reverse('service_detail', args=[service.slug]))
            else:
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
