# home/views.py
from django.shortcuts import render
from django.views import generic, View
from django.views.generic import ListView
from booking.models import Service
from reviews.models import Comment
from reviews.forms import CommentForm


class HomeView(ListView):
    model = Service
    template_name = 'home.html'
    context_object_name = 'service_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            approved=True)[:10]
        context['comment_form'] = CommentForm(
        ) if self.request.user.is_authenticated else None
        return context
