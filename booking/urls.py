# booking/urls.py
from .views import (
    ServiceDetail, BookServiceView, BookingsView,
    CancelBookingView, DeleteBookingView, AddCommentView,
    GetUnavailableTimes, EditBookingView
)
from django.urls import path

urlpatterns = [
    path(
        'get-unavailable-times/',
        GetUnavailableTimes.as_view(),
        name='get_unavailable_times'
    ),
    path(
        'book/<int:service_id>/',
        BookServiceView.as_view(),
        name='book_service'
    ),
    path(
        'bookings/',
        BookingsView.as_view(),
        name='view_bookings'
    ),
    path(
        'cancel-booking/<int:booking_id>/',
        CancelBookingView.as_view(),
        name='cancel_booking'
    ),
    path(
        'delete-booking/<int:booking_id>/',
        DeleteBookingView.as_view(),
        name='delete_booking'
    ),
    path(
        'edit-booking/<int:booking_id>/',
        EditBookingView.as_view(),
        name='edit_booking'
    ),
    path(
        'add-comment/',
        AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        '<slug:slug>/',
        ServiceDetail.as_view(),
        name='service_detail'
    ),
]
