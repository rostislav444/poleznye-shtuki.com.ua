from celery import shared_task
from apps.shop.models import CategoryImage, VariantImages
import os

@shared_task
def imagesRegen():  
    ImagesModels = [VariantImages]
    for model in ImagesModels:
        for image in model.objects.all():
            if image.image_sq == None:
                image.regen = True
                image.save()
    return True