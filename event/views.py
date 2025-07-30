from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Category
from .serializers import EventDetailSerializer, EventListSerializer

# Create your views here.


class EventListDetailsAPIView(APIView):

    def get(self, request):
        
        slug = request.query_params.get("slug")
        if slug:
            try:
                event = Event.objects.select_related('category').prefetch_related('attendees').get(slug=slug)
            except Event.DoesNotExist:
                return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = EventDetailSerializer(event)
            return Response(serializer.data)

        else:
            events = Event.objects.select_related('category').all()
            serializer = EventListSerializer(events, many=True)
            return Response(serializer.data)

    def post(self, request):
        title = request.query_params.get('title')
        description = request.query_params.get('description')
        category_name = request.query_params.get('category')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not title or not description or not category_name:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category_obj = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.create(
            title=title,
            description=description,
            category=category_obj,
            start_time=start_time,
            end_time=end_time
        )

        return Response({
            'message': 'Event created',
            'id': event.id,
            'slug': event.slug
        }, status=status.HTTP_201_CREATED)

class EventSearchView(APIView):
    def get(self,request):
        query = request.GET.get('q','')
        events = Event.objects.filter(title__icontains=query)
        serializer = EventListSerializer(events,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)