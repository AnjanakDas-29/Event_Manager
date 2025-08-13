from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Category(models.Model):
    
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.name

class Attendee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField( max_length=50)


    def __str__(self):
        return self.name

class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)
    
   
class Event(models.Model):
     title =models.CharField(max_length=50)
     description = models.TextField(max_length=450)
     location =models.CharField(max_length=50)
     start_time =models.TimeField(max_length=10)
     end_time= models.TimeField(max_length=10)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     attendees = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='registered_events',blank=True)
     slug = models.SlugField(unique=True,blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at =models.DateTimeField(auto_now=True)
     created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
     rsvp_limit =models.PositiveIntegerField(default=3)
     is_delete =models.BooleanField(default=False)

     objects=EventManager()
     all_objectts = models.manager
     

     class Meta:
         indexes = [
             models.Index(fields=['slug']),
             models.Index(fields=['start_time']),
             models.Index(fields=['location'])
         ]

     def save(self,*args, **kwargs):
        if not self.slug:
             self.slug = slugify(self.title)
        super().save(*args, **kwargs)

     def get_absolute_url(self):
        return reverse("event_details", kwargs={"slug": self.slug})
     
     def register_attendee(self,user):
         if self.attendees.count() >= self.rsvp_limit:
             raise ValidationError('Attendees limit reached')
         if user in self.attendees.all():
             raise ValidationError('you have already registered')
         self.attendees.add(user)

             

     def __str__(self):
         return self.title
    

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Attendee', 'Attendee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"












   

    

    
    

    



