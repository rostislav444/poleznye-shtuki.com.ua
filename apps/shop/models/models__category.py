from django.db import models
from django.urls import reverse
from apps.core.models import Image, NameSlug, Translation, Seo
from mptt.models import MPTTModel, TreeForeignKey


# CATEGORIES
class Category(Translation, NameSlug, Image, Seo, MPTTModel):
    parent =     TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родительская категория", related_name='children')
    taxonomy =   models.ForeignKey('shop.GoogleTaxonomy', on_delete=models.CASCADE, blank=True, null=True, help_text='Категория Google')
    num =        models.PositiveIntegerField(default=0, blank=True, verbose_name='Нумерация: Каталог')

    class MPTTMeta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        order_insertion_by = ['name']

    def save(self):
        super(Category, self).save()

    def __str__(self):
        return ' > '.join(self.tree_name)

    def get_absolute_url(self):
        return reverse('shop:catalogue', kwargs={ 'category' : '/'.join(self.tree_slug)})

    @property
    def tree_slug(self):
        return [category.slug for category in self.get_ancestors(include_self=True)]

    @property
    def tree_name(self):
        return [category.name for category in self.get_ancestors(include_self=True)]




 






   



