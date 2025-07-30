from django.shortcuts import render
from .models import  Event, Category
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class EventListDetailsView(View):
     
    def get(self,request,slug=None):
        if slug:
            try:
                event = Event.objects.select_related('category').prefetch_related('attendees').get(slug=slug)
            except Event.DoesNotExist:
                raise Http404("Event not found")

        
            event_data = {
                'title': event.title,
                'slug': event.slug,
                'description': event.description,
                'location': event.location,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'category': event.category.name,
                'attendees': [{'name': a.name, 'email': a.email} for a in event.attendees.all()]
            }

            return JsonResponse(event_data)
        else:
            events = Event.objects.select_related('category').all()
            data= []
            for event in events:
                data.append({
                'title' :event.title,
                'slug':event.slug,
                'category': event.category.name,
                'start_time' : event.start_time.isoformat()
            })
            
        return JsonResponse(data, safe=False)


    
    
    def post(self,request):
            if request.method == 'POST':
                title = request.POST.get('title')
                description = request.POST.get('description')
                location = request.POST.get('location')
                category = request.POST.get('category')
                start_time =request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                
                if not title or not description or not category:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
                category_obj = Category.objects.get(name=category)

                event= Event.objects.create(
                    title = title,
                    description = description,
                    location =location,
                    category = category_obj,
                    start_time = start_time,
                    end_time = end_time
                )
                
                return JsonResponse({
                    'message': 'Event created',
                    'id': event.id,
                    'slug': event.slug
                })
            return JsonResponse({'error': 'Only POST allowed'}, status=405)
    

class EventSearchView(View):
    def get(self,request):
        query = request.GET.get('q',' ')
        events =Event.objects.filter(title__icontains=query)

        data =[]
        for event in events:
            data.append({
                'id':event.id,
                'title':event.title,
                'description':event.description,
                'location': event.location,
                'start_time': event.start_time,
                'end_time': event.end_time

            })
        return JsonResponse(data,safe=False)