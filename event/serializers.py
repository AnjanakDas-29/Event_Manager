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
        fields = ['id','title', 'slug', 'description', 'location', 'start_time', 'end_time', 'category', 'attendees']


class EventListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',read_only=True)
    created_by =serializers.StringRelatedField(default=serializers.CurrentUserDefault(),read_only=True)
    

    class Meta:
        model = Event
        fields = ['id','title', 'slug', 'category', 'start_time','description', 'location','end_time', 'category_name','created_at','created_by','updated_at']

        

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model =Category
        fields = '__all__'


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
    

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user_obj= self.validated_data.get('user')

        username = user_obj['username']
        email = user_obj['email']
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        user = User.objects.filter(id=instance.user.id) 
        user.update(username=username, email=email) 
        return instance