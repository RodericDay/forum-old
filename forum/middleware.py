from django.http import HttpResponseRedirect
from django.conf import settings


class LoginRequiredEverywhereMiddleware:

    def process_request(self, request):
        if not request.user.is_authenticated():
            if request.path_info != '/login/':
                return HttpResponseRedirect('/login/')
