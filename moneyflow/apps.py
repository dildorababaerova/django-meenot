from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoneyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moneyflow'
    verbose_name= _("Rahavirrat")
