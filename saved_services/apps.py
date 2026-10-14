from django.apps import AppConfig
class SavedServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saved_services'

    def ready(self):
        import saved_services.signals