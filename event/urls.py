from .views import EventViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, EventViewSet,AttendeeEventRegisterView,CategoryViewSet,UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'category', CategoryViewSet, basename='category')




urlpatterns = [
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/<slug:slug>/register/',AttendeeEventRegisterView.as_view(), name='Attendee-Event-Register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]

urlpatterns += router.urls
