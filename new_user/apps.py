from django.apps import AppConfig

class New_UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'new_user'

    def ready(self) -> None:
        import new_user.signals