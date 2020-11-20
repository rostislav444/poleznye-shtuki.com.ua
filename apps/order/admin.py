from django.contrib import admin
from apps.order.models import Order, OrderProduct
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

class OrderProductInline(admin.TabularInline):
    def image(self, instance=None):
        if instance.pk:
            if   instance.variant: obj = instance.variant
            elif instance.product: obj = instance.product
            else: obj = None
            if obj:
                img = mark_safe("""<img style="object-fit: contain; object-position: center; border: 1px solid #ededed;" 
                    src="{url}" width="{width}" height={height} />""".format(
                        url = obj.image, width=240, height=240))
                return img
        else: return '-'

    model = OrderProduct
    extra = 0
    readonly_fields = ['image']
    fields = ['image','product','variant','quantity','price']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    readonly_fields = ['create']
    list_display = ['create', 'name', 'surname', 'patronymic', 'phone']

    fieldsets = ( 
        ('Покупатель',   {'fields' : ['name', 'surname', 'patronymic']}),
        ('Доставка',     {'fields' : ['city','region','branch_number']}),
        ('Контакты',     {'fields' : ['phone']}),
        ('Доп. инф.', {'fields' : ['create','comment']}),

    )
