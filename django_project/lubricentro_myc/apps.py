from django.apps import AppConfig


class LubricentroMycConfig(AppConfig):
    name = "lubricentro_myc"

    def ready(self):
        import lubricentro_myc.signals
