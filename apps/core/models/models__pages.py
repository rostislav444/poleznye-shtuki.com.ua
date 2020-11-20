from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse
from django import forms
from .models__translation import Translation
from .models__abstract import NameSlug
from ckeditor.fields import RichTextField
import unidecode





class Page(NameSlug, Translation):
    text =  RichTextField()

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def get_absolute_url(self):
        return reverse('core:page', kwargs={'slug':self.slug})

  


class Contacts(models.Model):
    email =  models.EmailField(blank=False, verbose_name='E-mail')
    name =   models.CharField(max_length=30, blank=False, verbose_name='Имя')
    text =   models.TextField(verbose_name='Сообщение')
    created =   models.DateTimeField(auto_now=True, null=True, verbose_name='Дата и время отправки')

    def __str__(self):
        time = self.created.strftime('%a %H:%M  %d/%m/%y')
        return ' - '.join([str(time) if self.created else '-', self.name, self.email])

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'