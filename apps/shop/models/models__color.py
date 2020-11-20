from django.db import models
from apps.core.models import Translation, Languages, Language
from apps.core.dict.hex_names import hex
from apps.core.dict.colors import colors
import webcolors
from colorfield.fields import ColorField
from googletrans import Translator
from apps.core.models import TranslatorsTranslate
from django.utils.text import slugify
from project.settings import BASE_DIR
from django.core.exceptions import ValidationError



def closest_color(requested_colour):
    min_colours = {}
    for key, value in colors.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(value)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = key
    color = min(min_colours.keys())    
    return min_colours[color]


def color_name(hex):
    requested_colour = webcolors.hex_to_rgb(hex)
    color_name = closest_color(requested_colour)
    return color_name


class Color(models.Model):
    hex =     ColorField(blank=True, null=True)
    name =    models.CharField(max_length=500, blank=True, null=True)
    name_en = models.CharField(max_length=500, blank=True, null=True, verbose_name="Цвет на английском")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f'{self.name} {str(self.hex)}'

    class Meta:
        verbose_name = 'Атрибут: Цвет'
        verbose_name_plural = 'Атрибуты: Цвета'
        ordering = ['name']

    def save(self):
        translator = Translator()
        if self.name or self.name_en:
            if self.name and not self.name_en:
                self.name_en = TranslatorsTranslate(text=self.name, language='en').capitalize().replace('-',' ')
            elif self.name_en and not self.name:
                self.name = TranslatorsTranslate(text=self.name_en, language='ru').capitalize()
            self.name_en = self.name_en.replace('-',' ')

            if not self.hex:
                try: self.hex = colors[self.name_en.lower()]
                except: 
                    raise ValidationError('Цвет не определен')

        elif self.hex:
            self.name_en = color_name(self.hex).capitalize()
            self.name = TranslatorsTranslate(text=self.name_en, language='ru', ignore=False).capitalize()
            self.hex = colors[self.name_en.lower()]
        else:
            raise ValidationError('Выберите цвет или введите его название')

        self.slug = slugify(self.name_en)
        super(type(self), self).save()





