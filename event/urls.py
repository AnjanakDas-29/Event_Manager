from django.urls import path
from .views import EventListDetailsAPIView,EventSearchView

urlpatterns = [
    path('events/', EventListDetailsAPIView.as_view()), 
    #path('events/<slug:slug>/', EventListDetailsAPIView.as_view()), 
    path('events/search/',EventSearchView.as_view()), 
]
