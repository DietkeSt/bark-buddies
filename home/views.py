# home/views.py
from django.shortcuts import render, redirect
from django.views import generic, View
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from booking.models import Service, Booking
from reviews.models import Comment
from reviews.forms import CommentForm


class HomeView(ListView):
    """
    View for displaying the home page with service list.
    """
    model = Service
    template_name = 'home.html'
    context_object_name = 'service_list'

    def get_queryset(self):
        """
        Return published services.
        """
        return Service.objects.filter(status=1)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the view.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            user_has_bookings = Booking.objects.filter(
                user=user, end_date__lt=timezone.now(), is_cancelled=False
            ).exists()
            context['user_has_bookings'] = user_has_bookings
        else:
            context['user_has_bookings'] = False

        context['comments'] = Comment.objects.filter(approved=True)[:10]
        context[
            'comment_form'
        ] = CommentForm() if user.is_authenticated else None
        return context


class SubmitHomeReview(View):
    """
    View for submitting comments on the home page.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle the post request to submit a comment.
        """
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            service_id = request.POST.get('service')
            service = Service.objects.get(id=service_id)
            new_comment = comment_form.save(commit=False)
            new_comment.service = service
            new_comment.name = request.user.username
            new_comment.approved = False
            new_comment.save()
            messages.success(
                request, "Thanks! Your comment is now being reviewed."
            )
        else:
            messages.error(
                request, "There was an error with your submission."
            )
        return redirect('home')
