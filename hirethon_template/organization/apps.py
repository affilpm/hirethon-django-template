from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hirethon_template.organization"
    
    def ready(self):
        import hirethon_template.organization.signals
