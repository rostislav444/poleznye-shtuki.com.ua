from django.db import models
from apps.core.models import Translation, Images


# PRODUCTS EQUIPMENT
class ProductEquipmentGroup(Translation, Images):
    parent = models.OneToOneField('shop.Product', on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True, default='',verbose_name='Текст')

    def __str__(self): return f'Преимущества {str(len(self.items.all()))}'

    class Meta:
        verbose_name = "Комплектация (группа)"
        verbose_name_plural = "Комплектация (группа)"


class ProductEquipment(models.Model):
    parent = models.ForeignKey('shop.ProductEquipmentGroup', on_delete=models.CASCADE, related_name='items')
    num = models.PositiveIntegerField(blank=True, default=None, null=True)
    name = models.CharField(max_length=255, blank=False)
    x = models.PositiveIntegerField(default=0)
    y = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('num','name',)
        verbose_name = "Комплектация"
        verbose_name_plural = "Комплектации"