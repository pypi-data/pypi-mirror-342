"""supply delivery app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SupplydeliveryConfig(AppConfig):
    """supply delivery app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dfhir.supplydelivery"
    verbose_name = _("Supply Delivery")
