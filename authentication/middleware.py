import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin


class AutoLogoutMiddleware(MiddlewareMixin):
    """
    Middleware pour la déconnexion automatique après une période d'inactivité.

    Méthodes:
        process_request (request): Vérifie la dernière activité et déconnecte si inactive.
    """

    def process_request(self, request):
        """
        Gère la déconnexion de l'utilisateur si la période d'inactivité dépasse SESSION_COOKIE_AGE.
        """
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
