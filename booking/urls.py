from . import views
from .views import ServiceList, ServiceDetail, book_service, view_bookings, cancel_booking, add_comment
from django.urls import path


urlpatterns = [
    path('', ServiceList.as_view(), name='home'),
    path('book/<int:service_id>/', book_service, name='book_service'),
    path('bookings/', view_bookings, name='view_bookings'),
    path('cancel-booking/<int:booking_id>/',
         cancel_booking, name='cancel_booking'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('<slug:slug>/', ServiceDetail.as_view(), name='service_detail'),
]
