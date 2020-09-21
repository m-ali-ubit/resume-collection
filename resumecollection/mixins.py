from django.db import models
from django.contrib import admin
from rest_framework.pagination import PageNumberPagination


class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ReadOnlyDateMixin(admin.ModelAdmin):
    readonly_fields = ("created_at", "last_updated_at")


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 50
