from apps.core.functions import *
from apps.shop.models import Variant
from apps.shop.models import Category
from apps.core.models import *
from project.settings import WISHLIST_SESSION_ID
import json


def categories(request):
    return {'categories' : Category.objects.all() }
 



def site_data(request):
    data = {
        'page_about' :  PageAbout.objects.all().first(),
        'page_delivery' : PageDelivery.objects.all().first(),
        'page_returns' : PageReturns.objects.all().first(),
        'page_guarantee' : PageGuarantee.objects.all().first(),
        'page_public_offer' : PagePublicOffer.objects.all().first(),
        'page_confidentiality' : PageConfidentiality.objects.all().first(),
    }
    return data

