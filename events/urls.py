from django.urls import path
from .views import EventListDetailsView, EventSearchView


urlpatterns = [
    path('events',EventListDetailsView.as_view() , name='event_list'),
    path('search/', EventSearchView.as_view(), name='search_events'),
    path('create_event',EventListDetailsView.as_view(),name='create_event'),
    
    path('<slug:slug>/', EventListDetailsView.as_view() , name='event_detail'),

]