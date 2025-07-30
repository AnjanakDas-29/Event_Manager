from rest_framework import serializers
from .models import Event, Category, Attendee  

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['name', 'email']

class EventDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    attendees = AttendeeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['title', 'slug', 'description', 'location', 'start_time', 'end_time', 'category', 'attendees']


class EventListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Event
        fields = ['title', 'slug', 'category', 'start_time']
