import pytz

from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone


class LoginRequiredEverywhereMiddleware:

    def process_request(self, request):
        if not request.user.is_authenticated():
            if request.path_info != '/login/':
                return HttpResponseRedirect('/login/')


class TimezoneMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            tz = pytz.timezone(request.user.profile.timezone)
            timezone.activate(tz)
            profile = request.user.profile
            profile.last_active = timezone.now()
            profile.save()
        else:
            timezone.deactivate()
