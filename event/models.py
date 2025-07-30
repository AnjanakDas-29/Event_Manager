from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField( auto_now_add=True)

class Attendee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class Event(models.Model):
     title =models.CharField(max_length=50)
     description = models.TextField(max_length=450)
     location =models.CharField(max_length=50)
     start_time =models.TimeField(max_length=10)
     end_time= models.TimeField(max_length=10)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     attendee = models.ManyToManyField(Attendee, related_name='Events')
     slug = models.SlugField(unique=True,blank=True)

     def save(self,*args, **kwargs):
        if not self.slug:
             self.slug = slugify(self.title)
        super().save(*args, **kwargs)

     def get_absolute_url(self):
        return reverse("event_details", kwargs={"slug": self.slug})
     
     def __str__(self):
         return self.title
     
    














   

    

    
    

    



