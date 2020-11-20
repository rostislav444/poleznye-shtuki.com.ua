from django.db import models
from .models__abstract import NameSlugText
from .models__translation import Translation
from .models__images import Images
from ckeditor.fields import RichTextField
import os
import cv2
import math
from project import settings
from django.conf.global_settings import LANGUAGES
from django.utils.text import slugify
import inspect
# TRANSLATORS
from django.utils.translation import get_language as lang
from googletrans import Translator
from textblob import TextBlob
import unidecode


        
        



# SITE TEXTS

class HomeSlider1(Translation, NameSlugText, Images):
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class HomeSlider2(Translation, NameSlugText, Images):
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class HomeSlider3(Translation, NameSlugText, Images):
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name




        





