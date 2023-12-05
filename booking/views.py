from django.shortcuts import render
from django.views import generic
from .models import Service


class ServiceList(generic.ListView):
    model = Service
    queryset = Service.objects.filter(status=1).order_by('title')
    template_name = 'index.html'
    paginate_by = 6
