from django.apps import AppConfig

class EhAppConfig(AppConfig):
    name = 'eh_app'

    def ready(self):
        super(EhAppConfig, self).ready()

        from .signals import fill_in_overall_fields, finalize_semester_statuses
