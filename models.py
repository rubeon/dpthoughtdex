from django.db import models
from taggit.managers import TaggableManager

import datetime

# Create your models here.

class Link(models.Model):
    """
    A link
    """
    url = models.URLField(blank=False)
    link_name = models.CharField(blank=True, max_length=255)
    message = models.TextField(blank=True)
    source = models.ForeignKey("Source")
    visible = models.BooleanField(default=True)
    excerpt = models.TextField(blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    author = models.ForeignKey("Author")
    tags = TaggableManager()
    
    def __unicode__(self):
        # how to repr myself
        return self.url
    

class Source(models.Model):
    """
    source of links
    """
    name = models.CharField(blank=True, max_length=255, unique=True)
    url = models.URLField(blank=True)
    icon = models.ImageField(upload_to="uploads/dpthoughtdex/links/", height_field="height", width_field="width")
    
    icon_height = models.IntegerField(blank=True, null=True)
    icon_width = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        # how to repr myself
        return self.name

class Author(models.Model):
    fullname = models.CharField(blank=True, max_length=255, unique=True)
    url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="uploads/dpthoughtdex/authors/", height_field="avatar_height", width_field="avatar_width")
    
    avatar_width = models.IntegerField(blank=True, null=True)
    avatar_height = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        # how to repr myself
        return self.fullname
        