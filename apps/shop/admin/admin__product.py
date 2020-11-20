from .globals import FORMFIELD_OVERRIDES, obj_link, obj_image, obj_image_url
from django.contrib import admin
from django import forms 
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms import TextInput, Textarea
from apps.shop.models import *
# Product childs
from .admin__product__equipment  import ProductEquipmentGroupInline
from .admin__feedback  import FeedbacksInline
from .admin__product__attrs  import ProductAttrGroupInline, CoreAdvantagesGroupInline
# Select
from easy_select2 import select2_modelform
from django.template.loader import render_to_string
from django.template import engines
from django.template import Template, Context


# PRODUCT IMAGES
class VariantImagesInline(admin.TabularInline):
    def image_preview(self, obj=None):
        if obj.pk:
            print(obj.image_thmb)
            img = mark_safe("""<img style="width:160px; height:160px; object-fit: cover; object-position: center; border: 1px solid #ededed;" 
                src="{url}" width="{width}" height={height} />""".format(url = obj.image_thmb['s']['path'], width=240, height=240))
            return img
        else: return '-'

    model = VariantImages
    readonly_fields = ['image_preview']
    fields = ['num','image_preview','image',]
    extra = 1


@admin.register(VariantImages)
class ProductImagesAdmin(admin.ModelAdmin):
    def image(self, obj=None):
        if obj.pk:
            try:
                img = mark_safe("""<img style="width:320px; height:320px; object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                    src="{url}" width="{width}" height={height} />""".format(url = obj.image_s.url, width=240, height=240))
                return img
            except: return '###'
        else: return '-'

    readonly_fields = ['image']
    list_display = ['pk','image',]

class ProdcutVideoInline(admin.TabularInline):
    model = ProdcutVideo
    extra = 0

class VariantForm(forms.ModelForm):
    model = Variant

    class Meta:
        fields = '__all__'


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 0    




class CoreAdvantagesInline(admin.TabularInline):
    model = CoreAdvantages
    extra = 0 

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    readonly_fields = ['image_preview']
    fields  = ['num','image_preview','image','show',]
    extra = 0
setattr(ProductImagesInline, 'image_preview', obj_image)



@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES

    def product(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj.parent._meta.app_label, obj.parent._meta.model_name), args=[force_text(obj.parent.pk)])
            url = '<a href="{url}" style="text-transform: uppercase;">Вернутся к продукту</a>'.format(url=url,text=' '.join([obj.parent.name, obj.parent.code]))
            return mark_safe(url)
        return '-'

    product.short_description = 'Ссылка на продукт'

    def image(self, obj=None):
        if hasattr(obj, 'images'):
            try:
                url = '<img style="width:240px; height:320px; object-fit: contain; object-position: center;" src="{url}">'.format(url=obj.images.all()[0].image_s.url)
                return mark_safe(url)
            except:return 'Нет фото'
        else:return '-'

    readonly_fields = ['product','view']
    list_display = ['image','price','old_price',]
    list_filter = ['parent__category','color']

    fieldsets = ( 
        ('Продукт',   {'fields' : ['product','parent']}),
        ('Вариант',   {'fields' : [('name','view'),'color',]}),
    )

    inlines = [
        VariantImagesInline,
    ]


class VariantInline(admin.TabularInline):
    def get_edit_link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            url = '<a href="{url}">{text}</a>'.format(url=url,text='Редактировать',)
            return mark_safe(url)
        return _("Нажмите сохранить и продолжить, для получения ссылки редактирования")

    def image(self, obj=None):
        try: 
            url = '<img style="width:240px; height:320px; object-fit: contain; object-position: center;" src="{url}">'.format(url=obj.images.all()[0].image_s.url)
            return mark_safe(url)
        except:return 'Нет фото'

    model = Variant
    change_form_template = 'admin/vendor/change_form.html'
    readonly_fields = ['get_edit_link','image']
    fields =  ['ordering','name','color','get_edit_link',]
    exclude = ['type']
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def product_image(self, obj=None):
        img_style = {
            'width' : '120px',
            'heught' : '120px',
            'object-fit' : 'cover',
            'object-position':'center',
            'box-shadow': '0 4px 8px rgba(0,0,0,0.15)',
            'margin-right': '16px',
            'margin-bottom': '16px',
            'border-radius' : '4px',
        }
        no_image = '/static/img/no_image.png'
        img_style = ''.join([f'{style}:{style_val};' for style, style_val in img_style.items()])

        if obj.pk:
            images = []
            
        
            variants = obj.variant.all()
            if len(variants):
                for variant in variants:
                    variant_image = variant.images.first()
                    if variant_image:
                        images.append(variant_image.image_thmb['s']['path'])
                    else:
                        images.append(no_image)
            else:
                if obj.image:
                    images.append(obj.image_thmb['s']['path'])
                elif obj.images.images.first():
                    images.append(obj.images.images.first().image_thmb['s']['path'])
                else:
                    images.append(no_image)


            images = ''.join([f'<img style="{img_style}" src="{url}">' for url in images])
            return mark_safe(images)
        else:
            return mark_safe(f'<img style="{img_style}" src="{no_image}">')
        

    def custom_label(self, obj=None):
        customlabels = ''
        if obj:
            for label in obj.customlabel.all():
                group = '#'
                if label.group:group = label.group.name
                item = '#'
                if label.item:item = label.item.name
                customlabels += ' '.join(['<p style="padding:0;">',group, ' - ',item, '</p>'])
            return mark_safe(customlabels)
        else:
            return customlabels

    def get_suplier_url(self, obj=None):
        if obj.suplier_url is not None:
            return mark_safe(f"<a href={obj.suplier_url}>На сайт поставщика</a>")
        return '-'

    fieldsets = ( 
        # ('SEO',      {'fields' : ['seo_title', 'seo_description', 'seo_keywords']}),
        ('BG',       {'fields' : ['bg1', 'bg2', 'slogan']}),
        ('Картинка', {'fields' : [('product_image','image')]}),
        ('Описание', {'fields' : ['category','name',('price','old_price'),('suplier_price','in_stock'),'gift','description','date',  ]}),
        ('Ссылки',   {'fields' : ['suplier','suplier_id',('get_suplier_url','suplier_url',)]}),
    )
    change_form_template = 'admin/shop/change_form.html'
    ordering = ('-date',)
    readonly_fields = ['product_image','get_suplier_url']
    list_filter =  ['category','variant__color']
    list_display = ['product_image','name','price','suplier_price']
    list_editable = ['date','price']
    list_display_links = ('product_image','name')
    formfield_overrides = FORMFIELD_OVERRIDES
    # change_form_template = 'admin/vendor/change_form.html'
    inlines = [
        # CoreAdvantagesGroupInline,
        ProductImagesInline,
        ProductSpecificationInline,
        # ProductAttrGroupInline,
        FeedbacksInline,
        ProductEquipmentGroupInline,
        VariantInline,
        ProdcutVideoInline,
    ]

