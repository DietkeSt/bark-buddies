# home/views.py
from django.shortcuts import render
from django.views import generic, View
from booking.models import Service


class HomeView(generic.ListView):
    model = Service
    queryset = Service.active.active_services()
    template_name = 'home.html'
