from django.contrib import admin
from .models import *


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    pass


@admin.register(HomeSlider1)
class HomeSlider1Admin(admin.ModelAdmin):
    list_display = ['name',]

@admin.register(HomeSlider2)
class HomeSlider2Admin(admin.ModelAdmin):
    list_display = ['name',]

@admin.register(HomeSlider3)
class HomeSlider3Admin(admin.ModelAdmin):
    list_display = ['name',]


# About us
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name','slug']



@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['email',]