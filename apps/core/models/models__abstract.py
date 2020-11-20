
from django.db import models
from django.contrib import admin
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from project import settings
from PIL import Image
# TRANSLATORS
from django.utils.translation import get_language as lang

import unidecode
import os
from django.apps import apps
import django
from django.contrib.contenttypes.models import ContentType
from shutil import copyfile
import jsonfield


class Seo(models.Model):
    seo_title =       models.CharField(max_length=70,  blank=True, null=True, help_text="До 70 символов",  validators=[MaxLengthValidator(70)])
    seo_description = models.TextField(max_length=300, blank=True, null=True, help_text="До 300 символов", validators=[MaxLengthValidator(300)])
    seo_keywords =    models.TextField(max_length=255, blank=True, null=True, help_text="До 255 символов", validators=[MaxLengthValidator(255)])

    class Meta:
        abstract = True


class NameSlug(models.Model):
    name =  models.CharField(max_length=300, blank=False, verbose_name="Название")
    slug =  models.CharField(max_length=320, blank=True, null=True, verbose_name="Иденитификатор", editable=False)

    class Meta:
        abstract = True

    def save(self):
        self.slug = slugify(unidecode.unidecode(self.name))
        super(NameSlug, self).save()


class NameSlugText(NameSlug):
    text =  models.TextField(blank=True, verbose_name="Текст")

    class Meta:
        abstract = True

 
class NameSlugChar(NameSlug):
    text =  models.CharField(blank=True, max_length=255, verbose_name="Текст")

    class Meta:
        abstract = True





           


    



