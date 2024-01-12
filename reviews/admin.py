# reviews/admin.py
from .models import Comment
from django.contrib import admin

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface options for Comment model.

    This class customizes the admin interface for the Comment model.
    It includes settings for display columns in the admin list view,
    filter options, search fields, and custom actions.
    """

    list_display = (
        'name',        # Name of the commenter
        'body',        # Content of the comment
        'service',     # The service to which the comment is associated
        'created_on',  # Date when the comment was created
        'approved'     # Whether the comment is approved or not
    )
    list_filter = (
        'approved',    # Filter by approved status
        'created_on'   # Filter by creation date
    )
    search_fields = (
        'name',        # Search by commenter's name
        'email',       # Search by commenter's email
        'body'         # Search within comment body
    )
    actions = ['approve_comments']

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form used in the admin interface for Comment model.

        This method overrides the default form to make the email field
        not required.
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['email'].required = False
        return form

    def approve_comments(self, request, queryset):
        """
        Custom admin action to approve comments.

        This action will mark selected comments as approved.
        """
        for obj in queryset:
            obj.approve()

    approve_comments.short_description = "Approve selected comments"
