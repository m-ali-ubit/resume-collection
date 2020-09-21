from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from resumecollection.mixins import CreateUpdateMixin


class User(AbstractUser, CreateUpdateMixin):

    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def set_new_username(self, username: str):
        self.username = username
        self.name = username
        self.save()
