from django.db import models
from apps.core.models import NameSlug
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from django.utils.translation import get_language as lang


# BRAND
class Brand(NameSlug):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/catalogue/' + self.slug
