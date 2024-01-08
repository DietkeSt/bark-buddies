"""barkbuddies URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('summernote/', include('django_summernote.urls')),
    path('', include('home.urls')),
    path('booking/', include('booking.urls')),
    path('accounts/', include('allauth.urls')),
]

