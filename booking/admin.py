from django import forms
from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from .models import Service, Booking, Availability, BookingTime
from reviews.models import Comment
from django_summernote.admin import SummernoteModelAdmin
from datetime import datetime, timedelta
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from django_summernote.models import Attachment
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialApp


# Unregister models
admin.site.unregister(SocialAccount)
admin.site.unregister(EmailAddress)
admin.site.unregister(Attachment)
admin.site.unregister(Site)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)


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
            obj.publish()

    publish_service.short_description = "Publish selected services"

    def unpublish_service(self, request, queryset):
        for obj in queryset:
            obj.unpublish()

    unpublish_service.short_description = "Unpublish selected services"


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('unavailable_from', 'unavailable_to')
    list_filter = ['unavailable_from', 'unavailable_to']


@admin.register(BookingTime)
class BookingTimeAdmin(admin.ModelAdmin):
    list_display = ('time',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'time_status',
        'service_status',
        'start_date_status',
        'end_date_status',
        'display_total_price',
        'cancellation_status',
    )
    list_filter = ['service', 'start_date', 'end_date', 'is_cancelled']
    search_fields = ['user__username', 'service__title']
    actions = ['cancel_bookings']

    def display_total_price(self, obj):
        return obj.service.price + obj.additional_price

    display_total_price.short_description = 'Total Price'

    def cancel_bookings(self, request, queryset):
        for booking in queryset:
            booking.cancel_booking()

    cancel_bookings.short_description = "Cancel selected bookings"

    def delete_bookings(self, request, queryset):
        for booking in queryset:
            booking.delete_booking()

    delete_bookings.short_description = "Delete selected bookings"

    def time_status(self, obj):
        if obj.is_cancelled:
            return format_html(
                '<span style="text-decoration: line-through;">{}</span>',
                obj.time
            )
        else:
            return obj.time

    def service_status(self, obj):
        if obj.is_cancelled:
            return format_html(
                '<span style="text-decoration: line-through;">{}</span>',
                obj.service
            )
        else:
            return obj.service

    def start_date_status(self, obj):
        if obj.is_cancelled:
            return format_html(
                '<span style="text-decoration: line-through;">{}</span>',
                obj.start_date
            )
        else:
            return obj.start_date

    def end_date_status(self, obj):
        if obj.is_cancelled:
            return format_html(
                '<span style="text-decoration: line-through;">{}</span>',
                obj.end_date
            )
        else:
            return obj.end_date

    def time_slot_status(self, obj):
        if obj.is_cancelled:
            return format_html(
                '<span style="text-decoration: line-through;">{}</span>',
                obj.time_slot
            )
        else:
            return obj.time_slot

    def cancellation_status(self, obj):
        if obj.is_cancelled:
            return format_html("Cancelled")
        else:
            return "Active"

    service_status.short_description = 'Service'
    start_date_status.short_description = 'Start Date'
    end_date_status.short_description = 'End Date'
    time_slot_status.short_description = 'Time Slot'
    cancellation_status.short_description = 'Status'
