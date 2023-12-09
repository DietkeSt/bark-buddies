from django.contrib import admin
from .models import Service, Comment, AvailableTime
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'price', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'title')
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'service', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['email'].required = False
        return form

    def approve_comments(self, request, queryset):
        for obj in queryset:
            obj.approved = True
            obj.save()

    approve_comments.short_description = "Approve selected comments"


class AvailableTimeInline(admin.StackedInline):
    model = AvailableTime
    extra = 1
