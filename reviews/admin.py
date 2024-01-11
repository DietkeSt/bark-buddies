# reviews/admin.py
from .models import Comment
from django.contrib import admin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'body',
        'service',
        'created_on',
        'approved'
    )
    list_filter = (
        'approved',
        'created_on'
    )
    search_fields = (
        'name',
        'email',
        'body'
    )
    actions = ['approve_comments']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['email'].required = False
        return form

    def approve_comments(self, request, queryset):
        for obj in queryset:
            obj.approve()

    approve_comments.short_description = "Approve selected comments"
