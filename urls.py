from django.conf.urls import patterns, include, url
from django.contrib import admin

from dpthoughtdex.models import Link

from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import DateDetailView

year_archive_pattern=r'^(?P<year>\d{4})/$'
month_archive_pattern=r'^(?P<year>\d{4})/(?P<month>\w{3})/$'
day_archive_pattern=r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$'


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'linker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', ArchiveIndexView.as_view(model=Link, date_field="pub_date"),name='link_list'),
    url(r'^upload/', 'dpthoughtdex.views.import_logfile', name="upload"),

)
