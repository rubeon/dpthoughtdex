from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse, Http404

from providers import irssi
from dpthoughtdex.forms import IrssiUploadForm
from dpthoughtdex.models import Link
import logging
import re
import datetime
# Create your views here.

logger = logging.getLogger(__name__)

# @login_required
def import_logfile(request, **kwargs):
    logger.debug("import_logfile entered")
    
    if request.method == "POST":
        logger.info("Received form submit, process log file")
        form = IrssiUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("form checked OK; processing")
            irssi.import_file(request)
            # return HttpResponseRedirect("/")
        else:
            logger.error(form.errors)
            c = RequestContext(request)
            c['form'] = form
            t = loader.get_template('upload.html')
            return HttpResponse(t.render(c))
    else:
        form = IrssiUploadForm()
    return render(request, "upload.html", {'form':form})

# @login_required
def add_message(username, password, source, message):
    # this will add a message to the list, and check
    # it for links
    # this view could be mapped to:
    # {'dpthoughtdex.views.add_message':'dpthoughtdex.add_message',}
    # client call would be :
    # s.dpthoughtdex.views.add_message(username, password, "#room", \
    #     "Freenode", "DPThought", "Check this out: http://google.com/")
    
    logger.debug("add_message entered")
    logger.debug("username: %s, password: %s, message: %s" % (username, password, message))
    
    # date and time, now or from the message?
    # :ehw!~eric@2001:4800:7815:105:7de7:84e6:ff05:86e7 PRIVMSG ##ericdev :heh http://www.meetup.com/UK-OSS-on-Windows-Azure-Platform-Meetup/events/220554498/
    # for raw IRC data, regex would be 
    irc_regex = irc_regex = "^:(?P<user>\w+)!~\w+@(?P<address>[\w+:.\-]*) (?P<command>\w+) (?P<room>[#\w\-_]+) :(?P<message>.*)$"
    res = re.match(irc_regex, message)

    if res:
        logger.debug(res.groups())
        user = res.group("user")
        command = res.group("command")
        room = res.group("room")
        message = res.group("message")
        
        url_matches = re.findall(irssi.url_regex, message)
        logger.debug(str(url_matches))
        for url in url_matches:
            # check if the author already exists
            author = irssi.get_author(user)
            source = irssi.get_source(source)
            d = {}
            d['author'] = author
            d['message'] = message
            d['source'] = source
            d['pub_date'] = datetime.datetime.now()

            for link in url_matches:
                d['url'] = link
                # check if this is a dup
                # dup's are defined as same pub_date + author + URL
                if irssi.get_link(d):
                    logger.info("got link %s that already exists" % str(d))
                    next
                
                l = Link(**d)
                logger.info("Created %s" % str(l))
                l.save()

        return True
    else:
        return False

