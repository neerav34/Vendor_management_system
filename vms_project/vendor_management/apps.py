from django.apps import AppConfig


class VendorManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendor_management'

# vendor_management/apps.py

from django.apps import AppConfig


class VendorManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_management"

    def ready(self):
        import vendor_management.signals  # Register signals

    def ready(self):
        import vendor_management.bussiness_logic
