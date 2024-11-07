# authentication/middleware.py

import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin


class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        now = datetime.datetime.now()
        last_activity = request.session.get('last_activity')

        if last_activity:
            delta = now - datetime.datetime.fromisoformat(last_activity)
            if delta.total_seconds() > settings.SESSION_COOKIE_AGE:
                logout(request)
                request.session.flush()  # Vide la session
        request.session['last_activity'] = now.isoformat()
