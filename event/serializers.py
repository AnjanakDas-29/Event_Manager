from rest_framework import serializers
from .models import Event, Category, Attendee  
from django.contrib.auth.models import User
from .models import UserProfile

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
    category_name = serializers.CharField(source='category.name',read_only=True)

    class Meta:
        model = Event
        fields = ['title', 'slug', 'category', 'start_time','description', 'location','end_time', 'category_name']




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
       
    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, role=role)
        return user