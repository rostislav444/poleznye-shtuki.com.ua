from .globals import ParentAdminRedirect, obj_link, obj_image, obj_image_url
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.urls import reverse
from apps.shop.models import Feedbacks, FeedbacksImages

class FeedbacksImagesInline(admin.TabularInline):
    model = FeedbacksImages
    readonly_fields = ['image_preview']
    fields  = ['num','image_preview','image',]
    extra = 0
setattr(FeedbacksImagesInline, 'image_preview', obj_image)


class FeedbacksInline(admin.TabularInline):
    def get_edit_link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            url = '<a href="{url}">{text}</a>'.format(url=url,text='Редактировать',)
            return mark_safe(url)
        return ("Нет объекта")

    model = Feedbacks
    extra = 0    
    readonly_fields = ['get_edit_link']
    fieldsets = ( 
        ('',   {'fields' : ['get_edit_link', 'gender','num','name','text']}),
    )


@admin.register(Feedbacks)
class FeedbacksAdmin(ParentAdminRedirect):
    inlines = [FeedbacksImagesInline]
    readonly_fields = ['image_preview']
    fieldsets = ( 
        ('',   {'fields' : [('gender','num','name')]}),
        ('',   {'fields' : [('image_preview','image')]}),
        ('',   {'fields' : ['text']}),
    )
setattr(FeedbacksAdmin, 'image_preview', obj_image)