from django.contrib import admin
from .models import Category, Attendee, Event
# Register your models here.

admin.site.register(Category)
admin.site.register(Attendee)
admin.site.register(Event)

class EventsAdmin(admin.ModelAdmin):
    list_display =('title','category','start_time')
    list_filter =('category','start_time')
    readonly_fields =['slug']
    search_fields =('title')







