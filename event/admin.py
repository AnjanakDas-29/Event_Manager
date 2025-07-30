from django.contrib import admin
from .models import Category,Attendee,Event

# Register your models here.
admin.site.register(Category)
admin.site.register(Attendee)
admin.site.register(Event)