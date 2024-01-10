"""barkbuddies URL Configuration"""

from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.urls import path, include
from .views import custom_404, custom_500

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('summernote/', include('django_summernote.urls')),
    path('', include('home.urls')),
    path('booking/', include('booking.urls')),
    path('accounts/', include('allauth.urls')),
]

handler404 = 'barkbuddies.views.custom_404'
handler500 = 'barkbuddies.views.custom_500'
