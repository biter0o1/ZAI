from django.apps import AppConfig


class FilmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "film"

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import film.signals