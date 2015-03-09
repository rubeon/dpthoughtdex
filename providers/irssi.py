# The irssi provider takes an irssi log file, and parses it into links
# a guid is generated using datetime + user + url, and would look like this;
# 2015-01-01-13-34-ehw-http://www.google.com/
# %Y-%m-%d-%H-%M-%(user)s-%(url)s
# it will look weird compared to others, but hey.

from dpthoughtdex.models import Link, Author, Source
from django.core.exceptions import ObjectDoesNotExist

import logging
import re
import tempfile
import datetime

irc_regex = "^(\d+):(\d+) < (\w+)>(.*)$"
url_regex = "https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
irc_pat = re.compile(irc_regex)

logger = logging.getLogger(__name__)

def get_author(user):
    # gets or creates an author
    logger.debug("get_author entered")
    try:
        author = Author.objects.get(fullname=user)
        logger.info("found author for '%s'" % user)
    except ObjectDoesNotExist, e:
        logger.warn("creating author '%s'" % user)
        author = Author(fullname=user)
        author.save()
    return author

def get_source(source_name):
    # gets or creates an author
    logger.debug("get_source entered")
    try:
        source = Source.objects.get(name=source_name)
        logger.info("found source for '%s'" % source_name)
    except ObjectDoesNotExist, e:
        logger.warn("creating source '%s'" % source_name)
        source = Source(name=source_name)
        source.save()
    return source

def get_link(props):
    logger.debug("get_link entered")
    l = Link.objects.filter(author=props['author'], url=props['url'], pub_date=props['pub_date'])
    if len(l):
        return True
    else:
        return False
    
class IrssiLog(object):
    
    """
    handles state for Irssi log files
    """
    cur_date = None
    source_name = None
    entries = []
    def __init__(self, logfile, source_name="Freenode"):
        logger.debug("IrssiLog()")
        logger.debug("Using %s" % logfile)
        self.logfile = logfile
        self.source_name = source_name
        # find the first usable date
        self.entries = logfile.readlines()
        logger.debug("Got %d lines of log" % len(self.entries))
        self.cur_date = self.get_first_date()
        logger.debug("Log starts on %s" % str(self.cur_date))
    
    def get_first_date(self):
        logger.info("get_first_date entered")
        curdate = self.cur_date
        for line in self.entries:
            logger.debug("Parsing %s" % str(line))
            if line.startswith("--- Day changed"):
                logger.debug("Got daychange")
                curdate = line.split("Day changed")[-1].strip()
                break
            elif line.startswith("-- Log"):
                # FIXME: this could probably be a regex, too
                logger.debug("Got Log open/close notification")
                start = len("-- Log opened") + 1
                curdate = line[start:].strip()
                break
        curdate = datetime.datetime.strptime(curdate, "%a %b %d %Y")
        return curdate
    
    def handle_daychanged(self, line):
        logger.info("handle_daychanged entered")
        newdate = datetime.datetime.strptime(line.split("Day changed")[-1].strip(), "%a %b %d %Y")
        if newdate != self.cur_date:
            self.cur_date = newdate
        logger.info("Day changed to %s" % self.cur_date.strftime("%a %b %d %Y"))
    
    def import_entries(self):
        # walks through all my entries, creating objects
        logger.debug("import_entries entered")
        for entry in self.entries:
            if entry.startswith("--- Day changed"):
                self.handle_daychanged(entry)
                next

            res = irc_pat.match(entry)
            if res:
                logger.debug(entry)
                hour, minute, user, message = res.groups()
                message = message.decode("latin-1")
                post_time = self.cur_date.replace(hour=int(hour), minute=int(minute)).strftime("%Y-%m-%d %H:%M")
                url_matches = re.findall(url_regex, message)
                logger.debug(str(url_matches))
                for url in url_matches:
                    # check if the author already exists
                    author = get_author(user)
                    source = get_source(self.source_name)
                    d = {}
                    d['author'] = author
                    d['message'] = message
                    d['source'] = source
                    d['pub_date'] = post_time
                    for link in url_matches:
                        d['url'] = link
                        # check if this is a dup
                        # dup's are defined as same pub_date + author + URL
                        if get_link(d):
                            logger.info("got link %s that already exists" % str(d))
                            next
                        l = Link(**d)
                        l.save()
                    # chef if the author already exists
                    
                
                
            
                
            

def import_file(request):
    """
    takes the form submission data from a 
    file upload, and processes the file
    """
    logger.debug("import_file entered")
    file = request.FILES['file']
    tmpfile = tempfile.TemporaryFile()
    for chunk in file.chunks():
        logger.info("writing %d bytes to %s" % (len(chunk), str(tmpfile)))
        tmpfile.write(chunk)
    
    tmpfile.seek(0)
    read_fd = tmpfile
    logger.info("done writing to %s" % str(tmpfile))
    res = parse_log(request.POST.get('source_name'), read_fd)
    return res
    

def parse_log(source, log_fd):
    """
    takes a source and file handle, and walks through it.
    
    Usually you would open a tempfile or so from your view, and pass it along with the source
    as arguments
    """
    logger.debug("parse_log entered")
    link_list = []
    ilog = IrssiLog(log_fd, source_name=source)
    
    # link_list = []
    
    ilog.import_entries()
    