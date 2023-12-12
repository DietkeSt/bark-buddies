from . import views
from .views import ServiceList, ServiceDetail, book_service, view_bookings, cancel_booking
from django.urls import path


urlpatterns = [
    path('', ServiceList.as_view(), name='home'),
    path('<slug:slug>/', ServiceDetail.as_view(), name='service_detail'),
    path('book/<int:service_id>/', book_service, name='book_service'),
    path('bookings/', view_bookings, name='view_bookings'),
    path('cancel-booking/<int:booking_id>/', cancel_booking,
         name='cancel_booking'),
]
