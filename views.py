from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse, Http404

from providers import irssi
from forms import IrssiUploadForm
import logging

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
