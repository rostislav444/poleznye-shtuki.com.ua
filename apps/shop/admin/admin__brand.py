from django.contrib import admin
from apps.shop.models import Brand
from .globals import *


# BRAND
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name',]
    readonly_fields = ['slug']
    formfield_overrides = FORMFIELD_OVERRIDES