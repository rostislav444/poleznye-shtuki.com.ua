from .globals import ParentAdminRedirect, FORMFIELD_OVERRIDES, obj_link, obj_image, obj_image_url, obj_parent_link
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.encoding import force_text
from apps.shop.models import LandingPage, CoreAdvantagesGroup, CoreAdvantages, ProductAttrGroup, ProductAttr






class CoreAdvantagesInline(admin.TabularInline):
    model = CoreAdvantages
    extra = 0
    readonly_fields = ['obj_image']
    fieldsets = ( 
        ('Основная информация', {'fields' : [('num','name','image','obj_image')]}),
    )
setattr(CoreAdvantagesInline, 'obj_image', obj_image)

@admin.register(CoreAdvantagesGroup)
class CoreAdvantagesGroupAdmin(ParentAdminRedirect):
    inlines = [CoreAdvantagesInline]
setattr(CoreAdvantagesGroupAdmin, 'parent_link', obj_parent_link)

class CoreAdvantagesGroupInline(admin.TabularInline):
    model = CoreAdvantagesGroup
    readonly_fields = ['link']
setattr(CoreAdvantagesGroupInline, 'link', obj_link)

class ProductAttrGroupInline(admin.TabularInline):
    model = ProductAttrGroup
    readonly_fields = ['link']
    fields = ['num','css','name','link']
    extra = 0
    # classes = ['attr_groups',]
setattr(ProductAttrGroupInline, 'link', obj_link)


class ProductAttrInline(admin.StackedInline):
    formfield_overrides = FORMFIELD_OVERRIDES
    model = ProductAttr
    extra = 0
    fieldsets = ( 
        ('', {'fields' : [('num','name','image')]}),
        ('', {'fields' : ['text']}),
    )
# setattr(ProductAttrInline, 'image', obj_image)

@admin.register(ProductAttrGroup)
class ProductAttrGroupAdmin(ParentAdminRedirect):
    formfield_overrides = FORMFIELD_OVERRIDES
    inlines = [ProductAttrInline]
    readonly_fields = ['parent_link']
    fields = ['parent_link','name',('num','css','image'),('text','text_after')]
setattr(ProductAttrGroupAdmin, 'parent_link', obj_parent_link)

@admin.register(LandingPage)
class LandingPageAdmin(ParentAdminRedirect):
    inlines = [
        ProductAttrGroupInline,
        CoreAdvantagesGroupInline,
    ]