# MODELS
from django.db import models
from django.apps import apps, AppConfig
from django.utils.translation import get_language as lang
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import redirect, reverse
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from project import settings
from apps.core.models import NameSlug, Images, Image, Seo, Translation, NameSlugChar
from apps.core.functions.functions__video import imageFromVideo, imagePathFK
from apps.shop.models.models__category import Category
from .models__product__equipment import ProductEquipmentGroup
from ckeditor.fields import RichTextField
from textblob import TextBlob
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from bs4 import BeautifulSoup
from project.settings import DROP1_API_TOKEN
import os, io, random, json, jsonfield, datetime, time, requests, urllib, unidecode
from colorfield.fields import ColorField



class Supliers():
    def __iter__(self):
        for suplier in [ (meth, meth) for meth in dir(self) if not meth.startswith('__')]:
            yield suplier
            
    def drop1(self, order, products):
        url = "https://drop1.top/api/ds_orders"
        api_key = DROP1_API_TOKEN

        data = {
            'name' : order.name,
            'lastname' : order.surname,
            'phone' : order.phone_number,
            'delivery_city' : order.city,
            'comment' : f'Отделение {order.branch_number}',
            'processing_type_id' : 2,
        }

        for n, product in enumerate(products):
            data[f'products[{n}][product_id]'] = product['product_id']
            data[f'products[{n}][quantity]'] = product['quantity']
            data[f'products[{n}][price]'] = product['price']

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept" : "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, params=data, headers=headers)
        return response.json()




class Product(Translation, Image, Seo):
    bg1 =                ColorField(blank=True, null=True, verbose_name="Цвет градиента 1")
    bg2 =                ColorField(blank=True, null=True, verbose_name="Цвет градиента 2")
    slogan =             models.TextField(blank=True, null=True, verbose_name="Слоган")
    suplier =            models.CharField(max_length=32, blank=True, null=True, choices=[x for x in Supliers()],)
    suplier_id =         models.CharField(max_length=32, blank=True, null=True)
    suplier_url =        models.CharField(max_length=500, blank=True, null=True)
    category =           models.ForeignKey('shop.Category', on_delete=models.PROTECT,  verbose_name="Категория товара", related_name='product')
    brand =              models.ForeignKey('shop.Brand', blank=True, null=True, on_delete=models.PROTECT, verbose_name="Бренд",  related_name='product')
    gift =               models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Подарок")
    code =               models.CharField(max_length=250, blank=True, verbose_name="Артикул")
    name =               models.CharField(max_length=250, blank=False, verbose_name="Название")
    slug =               models.CharField(max_length=250, blank=True,  verbose_name="Идентификатор")
    price =              models.PositiveIntegerField(default=0, blank=False, verbose_name="Цена")
    old_price =          models.PositiveIntegerField(default=0, blank=True,  verbose_name="Старая цена")
    suplier_price =      models.PositiveIntegerField(default=0, blank=True,  verbose_name="Входная цена")
    short_description =  models.TextField(blank=True, null=True, verbose_name="Короткое описание")
    description =        RichTextField(blank=True, null=True, verbose_name="Оисание")
    date =               models.DateTimeField(default=now, verbose_name="Дата загрузки")
    orders =             models.PositiveIntegerField(default=0, blank=True, verbose_name="Колличество заказов")
    stars =              models.FloatField(default=0, verbose_name='Рейтинг товара')
    sku =                models.CharField(max_length=250, blank=True, default='', editable=True, verbose_name="SKU")
    view =               models.PositiveIntegerField(default=0, verbose_name="Колличество просмотров")
    in_stock =           models.BooleanField(default=True)


    class Meta:
        ordering = ('-date',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return ' '.join([self.name, 'id:' + str(self.pk)])

    def get_sku(self):
        params = '_'.join([unidecode.unidecode(self.name)]) 
        params = slugify(params).replace('-','_')
        return params

    def translate(self):
        try: return self.translation.get(language__code=lang())
        except: return self

    def lp_url(self):
        return '/'

    @property
    def category_tree_slug(self):
        return '/'.join(self.category.tree_slug)
    
    def get_absolute_url(self):
        variants = self.variant.all()
        if len(variants):
            return variants.first().get_absolute_url()
        else:
            return reverse('shop:product', kwargs={
                'category' : self.category_tree_slug, 
                'slug' : self.slug, 
                'product_id' : self.pk
            })

    @property
    def get_discount(self):
        if self.old_price > self.price:
            return int((self.old_price - self.price) / self.old_price * 100)
        else: return 0

    @property
    def get_image(self):
        return self.imgs['image']['s']
       
    @property
    def get_image_xs(self):
        try:  return self.images.all().first().image_xs.url
        except: return '/static/img/no_image.png'

    @property
    def get_catalogue_url(self):
        variants = self.variant.all()
        context = {'slug' : self.slug,'product_id':self.pk,  'category' : self.category.slug, }
        if variants:
           context['variant_id'] = variants[0].pk
        return reverse('shop:product', kwargs=context)




    def get_catalogue_image(self):
        return ''
       
     
    def categories(self):
        categoriesList = []
        cateogry = self.category
        while cateogry != None:
            categoriesList.insert(0,cateogry)
            cateogry = cateogry.parent
        return categoriesList

    def save(self):
        self.slug = slugify(str(unidecode.unidecode(self.name)))
        self.sku = self.get_sku()
        soup = BeautifulSoup(self.description, 'html.parser')
        short_description = str('.'.join(soup.get_text().split('.')[:10]))
        for rplc in ['\n\n\n\n\n','\n\n\n\n','\n\n\n','\n\n','\n','... ','.. ','...','..']:
            short_description = short_description.replace('\n\n\n\n','. ')
        
        self.short_description = short_description
        super(Product, self).save()





class Feedbacks(Translation, Image):
    GENDER = (
        ('W', 'Ж'),
        ('M', 'M'),
    )
    parent =  models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Основное преимущество", related_name='feedbacks')
    gender =  models.CharField(choices=GENDER, default="W", max_length=255, verbose_name="Пол")
    num =     models.PositiveIntegerField(blank=True, default=None, null=True)
    name =    models.CharField(max_length=250, blank=False, verbose_name="Имя клиента")
    text =    models.TextField(blank=True, null=True, verbose_name="Текст")

    class Meta:
        ordering = ('num',)


class FeedbacksImages(Image):
    num =     models.PositiveIntegerField(blank=True, default=None, null=True)
    parent =  models.ForeignKey(Feedbacks, on_delete=models.CASCADE, verbose_name="Основное преимущество", related_name='images')

    class Meta:
        ordering = ('num',)


class ProductMainImage(Image):
    parent = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Изображения", related_name='main_image')


class ProductImages(Image):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Изображения", related_name='images')
    num =    models.PositiveIntegerField(blank=True, default=None, null=True)
    show =   models.BooleanField(default=True, verbose_name="Отображать в галереи")

    class Meta:
        ordering = ['-show','num']
        verbose_name = 'Изображения продукта'
        verbose_name_plural = 'Изображения продукта'


class ProductClientPhoto(Image):
    num = models.PositiveIntegerField(blank=True, default=None, null=True)
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Изображения", related_name='client_photo')
    show = models.BooleanField(default=True, verbose_name="Отображать в галереи")

    class Meta:
        ordering = ['-num']
        verbose_name = 'Фото клиентов'
        verbose_name_plural = 'Фото клиентов'


class Variant(models.Model):
    ordering =   models.PositiveIntegerField(blank=True, null=True)
    parent =     models.ForeignKey(Product,      on_delete=models.CASCADE, verbose_name="Продукт", related_name='variant')
    name =       models.CharField(max_length=250, blank=True, default='', verbose_name="Название")
    color =      models.ForeignKey('shop.Color', on_delete=models.SET_NULL, null=True, verbose_name='Цвет', blank=True, related_name='variant')
    sku =        models.CharField(max_length=250, blank=True, default='', editable=True, verbose_name="SKU")
    code =       models.CharField(max_length=250, blank=True, default='', verbose_name="Артикул")
    price =      models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена")
    old_price =  models.PositiveIntegerField(default=0, blank=True,  verbose_name="Старая цена")
    stock =      models.PositiveIntegerField(default=1, blank=True,  verbose_name="Остаток")
    date =       models.DateTimeField(default=now, verbose_name="Дата загрузки")
    view =       models.PositiveIntegerField(default=0, verbose_name="Колличество просмотров")
    
    class Meta:
        ordering = ('ordering',)
        verbose_name = 'Продукт: Вариация'
        verbose_name_plural = 'Продукт: Вариации'

    def __str__(self):
        name = ' - '.join([   
            str(self.parent.name).upper(),
            str(self.color.name if self.color else self.name).upper(),
        ])
        return name

    def translate(self):
        try: return self.translation.get(language__code=lang())
        except: return self

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={
            'category' : self.parent.category_tree_slug, 
            'slug' : self.parent.slug, 
            'product_id':self.parent.pk, 
            'variant_id':self.pk
        })

    def variant_price(self):
        if self.price > 0: return self.price
        else: return self.parent.price

    @property
    def image(self):
        image = self.images.first()
        if image: 
            return image.image_thmb['l']['path']
        return '/static/img/no-photo.png'

    @property
    def image_s(self):
        image = self.images.first()
       
        return '/static/img/no-photo.png'
        
    @property
    def get_image(self):
        try: self.images.first().image_s.url
        except: '/static/img/no-photo.png'

    @property
    def image_xs(self):
        image = self.images.first()
        if image: return image.image_thmb['xs']['path']
        return '/static/img/no-photo.png'


class VariantImages(Image):
    num = models.PositiveIntegerField(blank=True, default=None, null=True)
    parent = models.ForeignKey(Variant, on_delete=models.CASCADE, verbose_name="Обьем", related_name='images')
    show_feed = models.BooleanField(default=True, verbose_name="Отображать в фиде")

    class Meta:
        ordering = ('-num',)


class ProdcutVideo(models.Model):
    foreign_key =   models.ForeignKey('Product', on_delete=models.CASCADE, related_name='videos')
    upload_date =   models.DateTimeField(default=now, blank=True, editable=False)
    preload =       models.ImageField(blank = True)
    preload_old_url = models.CharField(blank=True, max_length=255, editable=True)
    video =         models.FileField(blank = False)
    video_old_url = models.CharField(blank=True, max_length=255, editable=True)

    class Meta:
        ordering = ('-upload_date',)
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return 'video-' + str(self.pk)

    def save(self, *args, **kwargs):
        if not self.video:
            self.video.name = imagePathFK(self.video, self.video.url, self.__class__.__name__)
            self.video_old_url = self.video.name
        else:
            if self.video.name != self.video_old_url:
                self.video.name = imagePathFK(self.video, self.video.url, self.__class__.__name__)
                if str(self.video_old_url) != '':
                    try:
                        os.remove(MEDIA_ROOT + self.video_old_url)
                    except: 
                        pass
                self.video_old_url = self.video.name
        super(type(self), self).save()
        videoPath = str(settings.MEDIA_ROOT) + str(self.video.name)
        path = str(self.video.name).split('.')[0]
        try:
            os.remove(settings.MEDIA_ROOT + self.preload_old_url)
        except: 
            pass
        self.preload.name = str(imageFromVideo(videoPath, path))
        self.preload_old_url = self.preload.name
        super(type(self), self).save()

    def delete(self):
        try:
            os.remove(MEDIA_ROOT + self.preload_old_url)
        except: pass
        super(type(self), self).delete()


class ProductSpecification(NameSlugChar, Translation):
    parent = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='specifications')



class ProductLandingPage(Product):
    class Meta:
        proxy = True

