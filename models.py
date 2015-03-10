from django.db import models
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
import logging
import datetime

# Create your models here.


logger = logging.getLogger(__name__)
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
        
    def get_absolute_url(self):
        logger.debug("get_absolute_url entered for %s" % self)
        # logger.debug("post_format: %s" % self.post_format)
        kwargs = {
            'pk': self.pk,
            'year': self.pub_date.year,
            'month': self.pub_date.strftime("%b").lower(),
            'day': self.pub_date.day,
        }
        return reverse("link-detail", kwargs=kwargs)
        
    

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
        