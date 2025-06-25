from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


    # 🔔 Automatically connect signals when app is ready
    def ready(self):
        import accounts.signals  # Signal for email verification, etc.

