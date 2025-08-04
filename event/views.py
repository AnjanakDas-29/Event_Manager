from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Category
from .serializers import EventDetailSerializer, EventListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from rest_framework import generics, permissions, filters
from django.contrib.auth.models import User
from .models import Event, UserProfile
from .serializers import RegisterSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
# Create your views here.




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class IsAdminOrReadOnly():
    pass

class EventPagination(PageNumberPagination):
    page_size = 5


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class =EventListSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title','slug']

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = EventPagination

    def get_serializer_class(self):             
        slug = self.request.query_params.get('slug')
        if slug:
            return EventDetailSerializer
        return EventListSerializer
           








