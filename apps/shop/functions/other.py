from django.utils.text import slugify
from project.settings import BASE_DIR
from django.utils.text import slugify
from PIL import Image
from unidecode import unidecode
import random
import datetime
import django
from django.core.files import File
import math
import os, cv2, math


def pluralName(name):
    consonant =   ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
    consonant_y = ['by','cy','dy','fy','gy','hy','jy','ky','ly','my','ny','py','qy','ry','sy','ty','vy','wy','xy','zy']
    vowel =   ['a', 'e', 'i', 'o', 'u']
    vowel_y = ['ay','ey','iy','oy','uy']
    if name[-1:] in consonant:
        name = str(name) + 's'
    elif name[-2:] in consonant_y:
        name = str(name)[:-1] + 'ies'
    elif name[-2:] in vowel:
        name = str(name)[:-1] + 's'
    elif name[-2:] in consonant_y:
        name = str(name)[:-1] + 'ies'
    return name





def imageResponsive(imgPath, size_name, size_px):
    img = Image.open(str(BASE_DIR) + str(imgPath))
    name = imgPath.rsplit('.')[0]
    ext  = imgPath.rsplit('.')[-1]
    if ext not in ['jpg', 'jpeg', 'gif', 'png']: sys.exit()
    img.thumbnail((size_px, size_px), Image.ANTIALIAS)
    filename = name + "_" + str(size_name) + "_" + str(size_px) + "." + str(ext)
    img.save(str(BASE_DIR) + filename, subsampling=0, quality=100, optimize=True)
    arr = filename.split('/')
    filename = arr[2] + '/' + arr[3]
    return filename



def imagePath(instance, file):
    slug_str = str(unidecode.unidecode(instance.name))
    slug_str = slugify(slug_str)
    filename = str(pluralName(instance.__class__.__name__)).lower() + '/%s.jpg' % (slug_str)
    return filename


# def imagePathFK(instance, filename, name_args, className = None):
#     slug=''
#     for num, arg in enumerate(name_args):
#         if num > 0:
#             slug += "_"
#         slug+=str(slugify(unidecode(arg)))
#     ext = filename.split('.')[-1]
#     if ext not in ['jpg', 'jpeg', 'gif', 'png', 'pdf']: sys.exit()
#     if className != None:
#         path = className
#     else:
#         path = instance.__class__.__name__
#     time = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
#     file_name = str(path).lower() + '__' + slug + '__' + str(random.randrange(1000, 9999, 1))
#     full_path = str(path) + '/' + str(file_name) + '.' + str(ext)
#     return full_path

def imagePathFK(instance, filename, className = None):
    ext = filename.split('.')[-1]
    if className != None:
        path = className
    else:
        path = instance.__class__.__name__
    time = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    file_name = str(path).lower() + '__' + time + '__' + str(random.randrange(1000, 9999, 1))
    full_path = str(path) + '/' + str(file_name) + '.' + str(ext)
    return full_path







def countPagination(page, prod_qnt, per_page):
    pages = math.ceil(prod_qnt / per_page)
    data = {
        'prev' : { 'active' : True },
        'next' : { 'active' : True },
        'num_first' : { 'active' : False },
        'num_last'  : { 'active' : False},
        'dots_prev' : { 'active' : False },
        'dots_next' : { 'active' : False },
        'nums'      : [],
        'last_page' : pages
    }
    if page == 1:
        data['prev']['active'] = False
    if page == pages:
        data['next']['active'] = False
    if page > 2 and pages > 5:
        data['num_first']['active'] = True
        data['dots_prev']['active'] = True
    if page < (pages - 3) and pages > 5:
        data['num_last']['active'] = True
        data['dots_next']['active'] = True

    if (page > 3 or page < (pages - 3)) and pages > 5:
        for i in range(page-1, page+2):
            if i > 0:
                if i == page:
                    data['nums'].append({ 'num' : i, 'active' : True })
                else:
                    data['nums'].append({ 'num' : i, 'active' : False })
    else:
        for i in range(1, pages+1):
            if i == page:
                data['nums'].append({ 'num' : i, 'active' : True })
            else:
                data['nums'].append({ 'num' : i, 'active' : False })
    return data




    # def pagination2(page, prod_qnt, per_page):
    #     pages = math.ceil(prod_qnt / per_page)
    #     product_sart = (page - 1) * per_page
    #     product_end =  (page - 1) * per_page





    #     return





    #  attrs = {
    #         'product' : [
    #             'brand',
    #             'filters'
    #         ],
    #         'variant' : ['color', 'sizes'],

    #     }



    #     QueryParams = Q()
    #     # COLLECT FILTER PARAMS IN QUERY
    #     for key, value in attrs.items():
    #         add = ''
    #         if key == 'product':
    #             add = 'parent__'
    #         for attr in value:
    #             params = kwargs[attr]
    #             if params != None:
    #                 params = params.split(',')
    #                 QueryParams &= Q(**{add + attr + '__slug__in':params})
    #                 if attr in self.context.keys():
    #                     for item in self.context[attr]:
    #                         if item.slug in params:
    #                             item.checked = True

    #  # MAKE QUERY
    #     self.context['variants'] = self.context['variants'].filter(QueryParams)
