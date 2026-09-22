from django.conf import settings
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        if not settings.DEBUG:
            from django.contrib.auth.models import update_last_login
            from django.contrib.auth.signals import user_logged_in

            user_logged_in.disconnect(update_last_login)
