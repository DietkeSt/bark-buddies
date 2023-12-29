# home/urls.py
from django.urls import path
from .views import HomeView, SubmitHomeReview

urlpatterns = [
    path(
        '', HomeView.as_view(), name='home'
    ),
    path(
        'submit-review/', SubmitHomeReview.as_view(), name='submit_home_review'
        ),
]
