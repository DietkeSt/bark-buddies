# reviews/models.py
from django.db import models
from booking.models import Service


class Comment(models.Model):
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
        ordering = ['created_on']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    @classmethod
    def create_comment(
        cls,
        user,
        form_data
    ):
        comment = cls(
            name=user.username,
            email=user.email,
            **form_data
        )
        comment.save()
        return comment
