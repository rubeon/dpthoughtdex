from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from dpthoughtdex.models import Link

class LatestEntriesFeed(Feed):

    title = "DPThoughtDex Feed"
    # link = reverse("link-list-day")
    link = "http://dev.ehw.io/"
    
    def items(self):
        return Link.objects.order_by('-pub_date')[:50]
    
    def item_title(self, item):
        res = "%s: %s"
        return res % (item.author, item.url)
    
    def item_description(self, item):
        return item.message
    
