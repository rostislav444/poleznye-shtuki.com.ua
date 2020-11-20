from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Order(models.Model):
    name = models.CharField(blank=False, max_length=500, verbose_name="Имя")
    surname = models.CharField(blank=True, max_length=500, verbose_name="Фамилия")
    patronymic = models.CharField(blank=True, max_length=500, verbose_name="Отчество")
    phone_number = models.CharField(max_length=50, verbose_name="Телефон (только цифры)", editable=False)
    phone = models.CharField(max_length=500, verbose_name="Телефон")
    create = models.DateTimeField(default=timezone.now, verbose_name="Время заказа")
    comment = models.TextField(blank=True)
    # NP
    city = models.CharField(blank=False, max_length=500)
    region = models.CharField(blank=True, max_length=500)
    branch_number = models.CharField(blank=False, max_length=500)

    def __str__(self):
        return ' - '.join([self.create.strftime("%H:%M %d.%m.%Y"), self.city, self.branch_number, self.phone])

    class Meta:
        ordering = ['-create']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('shop.Variant', blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    
    @property
    def total(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = 'Заказ: Товар'
        verbose_name_plural = 'Заказ: Товары'

    def __str__(self):
        return ' - '.join([self.product.name, self.variant.color.name if self.variant else '', str(self.quantity), str(self.price)])

