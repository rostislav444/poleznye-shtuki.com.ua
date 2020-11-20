from .globals import ParentAdminRedirect, FORMFIELD_OVERRIDES, obj_link, obj_image, obj_image_url, obj_parent_link
from django.contrib import admin
from apps.shop.models import ProductEquipmentGroup, ProductEquipment


# EQUIPMENT
class ProductEquipmentGroupInline(admin.StackedInline):
    model = ProductEquipmentGroup
    readonly_fields = ['link']
    fields = ['link']
    extra = 0
    # classes = ['attr_groups',]
setattr(ProductEquipmentGroupInline, 'link', obj_link)


class ProductEquipmentInline(admin.TabularInline):
    model = ProductEquipment
    extra = 1

@admin.register(ProductEquipmentGroup)
class ProductEquipmentGroupAdmin(admin.ModelAdmin):
    inlines = [ProductEquipmentInline]
    readonly_fields = ['parent_link']
   
setattr(ProductEquipmentGroupAdmin, 'parent_link', obj_parent_link)
