from django.contrib import admin
from apps.shop.models.models__color import *



@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass