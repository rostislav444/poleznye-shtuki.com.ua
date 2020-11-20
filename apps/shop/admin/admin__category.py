from django.contrib import admin
from django import forms 
from apps.shop.models import Category, GoogleTaxonomy, GoogleTaxonomyUplaoder
from .globals import FORMFIELD_OVERRIDES, obj_image
from .globals import *
from django.utils.safestring import mark_safe


# CATEGORIES
@admin.register(GoogleTaxonomy)
class GoogleTaxonomyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(GoogleTaxonomyUplaoder)
class GoogleTaxonomyUplaoderAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def tree(self, obj):
        if obj.pk:
            return ' > '.join(obj.tree_name)
        return None
        
    tree.short_description = "Название"

    formfield_overrides = FORMFIELD_OVERRIDES
    readonly_fields = ['obj_image','tree']
    list_display = ['obj_image','tree','num',]
    list_editable = ['num',]
    ordering = ('-parent__name','name',)
    fieldsets = (
        (None, {'fields' :  ['parent','name',('image','obj_image'),'taxonomy','num']}),
        ('SEO', {'fields' : ['seo_title', 'seo_description', 'seo_keywords']}),
    )
setattr(CategoryAdmin, 'obj_image', obj_image)
