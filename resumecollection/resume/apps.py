from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResumeConfig(AppConfig):
    name = "resumecollection.resume"
    verbose_name = _("Candidates")
