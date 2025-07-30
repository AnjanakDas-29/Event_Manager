from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=20)
    created_at =models.DateTimeField(auto_now=True)


class Attendee(models.Model):
    name = models.CharField(max_length=20)
    email= models.EmailField(max_length=25)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Attendee, related_name='events')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


