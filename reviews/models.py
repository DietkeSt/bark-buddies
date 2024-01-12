# reviews/models.py
from django.db import models
from booking.models import Service


class Comment(models.Model):
    """
    Model representing a comment on a service.
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)
    body = models.TextField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """
        Meta options for Comment model.
        """
        ordering = ['created_on']

    def approve(self):
        """
        Approve the comment.
        """
        self.approved = True
        self.save()

    def __str__(self):
        """
        String representation of the Comment.
        """
        return f"Comment {self.body} by {self.name}"

    @classmethod
    def create_comment(cls, user, form_data):
        """
        Create a comment from form data.
        """
        comment = cls(
            name=user.username,
            email=user.email,
            **form_data
        )
        comment.save()
        return comment
