from rest_framework import serializers
from apps.shop.models.models__product import Product, Variant


class ProductCartSerializer(serializers.ModelSerializer):
    id =    serializers.IntegerField(source="pk")
    link =  serializers.CharField(source="get_absolute_url")
    image =      serializers.CharField(source="image_thmb.s.path")

    class Meta:
        model = Product
        fields = ['id','name','link','image']



class VariantCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="parent.pk")
    variant_id = serializers.IntegerField(source="pk")
    color =     serializers.SerializerMethodField()
    price =      serializers.IntegerField(source="parent.price")
    old_price =  serializers.IntegerField(source="parent.old_price")
    # link =       serializers.CharField(source="get_absolute_url")
    image =      serializers.CharField(source="image_xs")

    class Meta:
        model = Variant
        fields = ['product_id', 'variant_id', 'name', 'color', 'price', 'old_price', 'image', ]

    def get_color(self, obj):
        if obj.color:
            return {
                'name' : obj.color.name,
                'hex'  : obj.color.hex
            }
        return None

    

class VariantSerializer(serializers.ModelSerializer):
    id =        serializers.IntegerField(source="pk")
    color =     serializers.SerializerMethodField()
    image =     serializers.SerializerMethodField()
    url =      serializers.CharField(source="get_absolute_url")

    class Meta:
        model = Variant
        fields = ['id', 'name', 'color', 'price', 'old_price', 'url', 'image']

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return image.image_thmb
        return None
    
    def get_color(self, obj):
        if obj.color:
            return {
                'name' : obj.color.name,
                'hex'  : obj.color.hex
            }
        return None

    

class ProductSerializer(serializers.ModelSerializer):
    id =       serializers.IntegerField(source="pk")
    name =     serializers.CharField(source="translate.name")
    url =      serializers.CharField(source='get_absolute_url')
    image =    serializers.SerializerMethodField()
    discount = serializers.CharField(source="get_discount")
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','name','price','old_price','url','discount','lp_url','image','variants']

    def get_variants(self, obj):
        variants = VariantSerializer(obj.variant.all(), many=True, read_only=True)
        return variants.data

    def get_image(self, obj):
        variant = obj.variant.first()
        if variant:
            variant_image = obj.variant.first().images.first()
            if variant_image:
                return variant_image.image_thmb['s']['path']
        if obj.image:
            return obj.image_thmb['s']['path']
        product_image = obj.images.first()
        if product_image:
            return product_image.image_thmb['s']['path']
        return '/static/img/no_image.png'

 



