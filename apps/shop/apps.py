from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'apps.shop'

    def ready(self):
        model = self.get_model('Product')
       
