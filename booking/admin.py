from django.contrib import admin
from .models import Service
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'title')
    summernote_fields = ('content')
