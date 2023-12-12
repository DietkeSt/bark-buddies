from django.contrib import admin
from .models import Service, Comment, Booking, TimeSlot
from django_summernote.admin import SummernoteModelAdmin
from datetime import datetime, timedelta


@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'price', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'title')
    summernote_fields = ('content')
    actions = ['publish_service', 'unpublish_service']

    def publish_service(self, request, queryset):
        for obj in queryset:
            obj.status = 1
            obj.save()

    publish_service.short_description = "Publish selected services"

    def unpublish_service(self, request, queryset):
        for obj in queryset:
            obj.status = 0
            obj.save()

    publish_service.short_description = "Unpublish selected services"


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


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['time_of_day', 'limit']
    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = ('user', 'service', 'start_date',
                    'end_date', 'time_slot', 'comments')
    list_filter = ['service', 'start_date', 'end_date']
    search_fields = ['user__username', 'service__title']
    actions = ['cancel_bookings']

    def display_time_slots(self, obj):
        return ", ".join(map(str, obj.time_slots.all()))

    display_time_slots.short_description = 'Time Slots'

    def cancel_bookings(self, request, queryset):
        for booking in queryset:
            booking.cancel()

    cancel_bookings.short_description = "Cancel selected bookings"
