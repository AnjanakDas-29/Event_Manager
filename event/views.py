from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Event, Category
from .models import Event, UserProfile
from .serializers import RegisterSerializer,CategorySerializer
from .serializers import EventDetailSerializer, EventListSerializer,UserProfileUpdateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from event.permissions import IsAdminOrReadOnly
from event.pagination import EventPagination
# Create your views here.




class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class EventViewSet(ModelViewSet):

    queryset = Event.objects.all()
    serializer_class =EventListSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title','slug']
    ordering  = ['start_time','created_at']

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = EventPagination

    def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)

    def destroy(self,request,*args,**kwargs):
        instance =self.get_object()
        instance.is_delete = False
        instance.save()
        return Response({'message':'Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):             
        slug = self.request.query_params.get('slug')
        if slug:
            return EventDetailSerializer
        return EventListSerializer
    
        
    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        start_time = self.request.query_params.get('start_time',None)
        location = self.request.query_params.get('location',None)

        queryset= Event.objects.all()

        if category is not None:
            queryset=Event.objects.filter(category__name=category)
        if start_time is not None:
            queryset = Event.objects.filter(start_time=start_time)
        if location is not None:
            queryset = Event.objects.filter(location__icontains=location)
        return queryset

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_events(self, request):
        now = timezone.now()
        events = Event.objects.filter(start_time__gte=now).order_by('start_time')
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'],url_path='previous')
    def past_events(self,request):
        now =timezone.now
        events = Event.objects.filter(start_time_lt=now).order_by('start_time')
        serializer = self.get_serializer(events,many=True)
        return Response(serializer.data)
    
        

class AttendeeEventRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,slug):
        event = get_object_or_404(Event, slug=slug)
        try:
            event.register_attendee(request.user)
            return Response({'detail': 'Successfully registered'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        

    

class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes=[IsAdminOrReadOnly]



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    

