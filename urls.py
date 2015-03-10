from django.conf.urls import patterns, include, url
from django.contrib import admin

from dpthoughtdex.models import Link
from dpthoughtdex.feeds import LatestEntriesFeed

from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import DateDetailView

year_archive_pattern=r'^(?P<year>\d{4})/$'
month_archive_pattern=r'^(?P<year>\d{4})/(?P<month>\w{3})/$'
day_archive_pattern=r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$'
link_detail_pattern = r'(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<pk>\d+)/$'
PAGE_LENGTH=10

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'linker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(link_detail_pattern, DateDetailView.as_view(model=Link, date_field="pub_date",), name='link-detail'),
    url(month_archive_pattern, DayArchiveView.as_view(model=Link,paginate_by=PAGE_LENGTH, date_field="pub_date"),name='link-list-month', ),
    url(day_archive_pattern, DayArchiveView.as_view(model=Link,paginate_by=PAGE_LENGTH, date_field="pub_date"),name='link-list-day', ),

    url(r'^$', ArchiveIndexView.as_view(model=Link,paginate_by=PAGE_LENGTH, date_field="pub_date"),name='link-list', ),
    url(r'^upload/', 'dpthoughtdex.views.import_logfile', name="upload"),
    url(r'^feed/$', LatestEntriesFeed()),

)
