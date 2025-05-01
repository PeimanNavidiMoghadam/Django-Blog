from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone

from .mixins import UniqueSlugMixin
import os
from uuid import uuid4

class Category(models.Model):
    slug_from_field = 'name'
    
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True , blank=True)
    

    def __str__(self):
        return self.name
   
   
    
class Tag(models.Model):
    slug_from_field = 'name'
    
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True)


    def __str__(self):
        return self.name



def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join("thumbnails", str(instance.pk or 'temp'), filename)
    


class Post(models.Model):
    slug_from_field = 'title'
    
    class Status(models.TextChoices):
        DRAFT = 'D', 'Draft'
        PUBLISHED = 'P', 'Published'
        
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'               
                               )
    thumbnail = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        default="thumbnails/default.jpg"
        )
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True) 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)


    
    class Meta:
        indexes = [
            models.Index(fields=['status', '-created']),
            models.Index(fields=['status', 'category', '-created']),
        ]
        
        
    def __str__(self):
        return self.title



class Comment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'
        
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        unique_together =('user', 'post')
        
        
    def __str__(self):
        return f"{self.user} liked {self.post}"