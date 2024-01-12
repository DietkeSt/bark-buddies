# reviews/apps.py
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Configuration class for the 'reviews' app.

    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
