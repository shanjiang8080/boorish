from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete

class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'
    def ready(self):
        from . import signals

        post_save.connect(signals.rename_callback)
        pre_delete.connect(signals.delete_callback)
        # wanted to clean leading/trailing spaces but dunno how. i'll just add it to the validator for now.