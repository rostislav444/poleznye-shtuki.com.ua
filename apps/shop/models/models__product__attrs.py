from django.db import models
from apps.core.models import Translation, Images, Image
from ckeditor.fields import RichTextField


class LandingPage(models.Model):
    product =    models.OneToOneField('shop.Product', on_delete=models.CASCADE, verbose_name="Продукт", related_name='lp')


class CoreAdvantagesGroup(models.Model):
    CSS = (
        ('image_list',  'Список с картинками'),
        ('point_list',  'Список с точками'),
        ('number_list', 'Список с номерами'),
    )
    css =       models.CharField(max_length=255, choices=CSS, blank=False, null=True)
    parent =    models.OneToOneField('shop.LandingPage', on_delete=models.CASCADE, verbose_name="Основное преимущество", related_name='advantages_group')

    def __str__(self):
        return "Основыне преимущества"

    class Meta:
        verbose_name = "Группа преимузеств"
        verbose_name_plural = 'Группа преимузеств'

class CoreAdvantages(Translation, Image):
    parent =    models.ForeignKey(CoreAdvantagesGroup, on_delete=models.CASCADE, verbose_name="Основное преимущество", related_name='advantages')
    num =       models.PositiveIntegerField(blank=True, default=None, null=True)
    name =      models.CharField(max_length=250, blank=False, verbose_name="Название")

    class Meta:
        ordering = ('num',)
        verbose_name = "Основыне преимущества"
        verbose_name_plural = 'Основыне преимущества'


class ProductAttrGroup(Translation, Image):
    CSS = (
        ('function', 'Функции'),
        ('advantage', 'Номерованный список'),
        ('side_by_side', 'Картинки по краям'),
        ('key_value', 'Список в 2 колонки' ),
    )
    num =        models.PositiveIntegerField(blank=True, default=None, null=True)
    css =        models.CharField(max_length=255, choices=CSS, blank=False, null=True)
    parent =     models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='attrs')
    name =       models.CharField(max_length=255, blank=True, null=True)
    text =       RichTextField(blank=True, null=True, default='', verbose_name="Текст")
    text_after = RichTextField(blank=True, null=True, default='', verbose_name="Текст после")

    def __str__(self): 
        return f'Attr {str(len(self.items.all()))}'

    class Meta:
        ordering = ('num',)


class ProductAttr(Translation, Image):
    num =    models.PositiveIntegerField(blank=True, default=None, null=True)
    parent = models.ForeignKey('shop.ProductAttrGroup', on_delete=models.CASCADE, related_name='items')
    image =  models.FileField(blank=True,null=True, verbose_name="Изображение")
    name =   models.CharField(max_length=500, blank=True, null=True)
    text =   models.TextField(blank=True, default='')
   
    class Meta:
        ordering = ('num',)
        # verbose_name = "Преимущество"
        # verbose_name_plural = 'Преимущества'


