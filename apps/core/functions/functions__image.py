import os
import PIL
from unidecode import unidecode
from project import settings
from django.utils.text import slugify
from project import settings
import shutil
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def tempImagePath(instance, filename):
    ext = filename.split('.')[-1]
    return settings.MEDIA_ROOT + 'temp.' + ext


def imageSizes(self, image):
    if image.name is None: return
    root = settings.MEDIA_ROOT
    imageSizes = {'l':  1920,'m':  1080,'s':  480,'xs': 240,'sq': 1200}
    ext =  str(image.name.split('.')[-1]).lower()
    
    def get_model_sizes(self):
        sizes = []
        for field in self._meta.fields:
            field = field.name
            if 'image' in field and 'url' not in field:
                sizes.append(field.replace('image_',''))
        return sizes
    
    # Get sizes keys from model fields names
    sizes = get_model_sizes(self)

    def get_name(self):
        # For better SEO we need human readeble imge name
        obj = self
        name_parts = []
        name_fields = ['slug','title','name']
        while obj != None:
            for field in name_fields:
                if hasattr(obj, field):
                    attr = getattr(obj, field)
                    if attr is not None:
                        name_parts.insert(0, slugify(unidecode(attr))) 
                        break
            if hasattr(obj, 'parent'):
                obj = obj.parent
            else: break
        name = '_'.join(name_parts)[:60]
        name +=  "_" + str(self.pk)
        return name

    def get_path(self):
        path = ''
        for level in [self._meta.app_label, self._meta.model_name]:
            path += level + '/'
            if not os.path.isdir(root + path): 
                os.mkdir(root + path)
        return path

    def add_png_alpha(image):
        # Somtimes people save png images, that has no transperancy level
        # that couse PIL errror. So we need add it.
        background = PIL.Image.new("RGBA", image.size, (0,0,0,0))
        background.paste(image)
        return background

    def make_square(image, min_size=1200):  
        pass

    def make_thumb(image, filename, size):
        if size in imageSizes.keys():
            res = imageSizes[size] 
            image = PIL.Image.open(image)
            if ext == 'png': image = add_png_alpha(image)
            image.thumbnail((res, res), PIL.Image.ANTIALIAS)
            image.save(root + filename, quality=100)
            image.close()

    def make_thumbs(self, image):
        name, path = get_name(self), get_path(self)
        for size in sizes:
            if ext == 'gif':
                filename =  f'{path}{name}.{ext}'
                if size == 'l': 
                    shutil.copyfile(image.path, root + filename)
            else: 
                filename =  f'{path}{name}_{size}.{ext}'
                make_thumb(image, filename, size)
            setattr(getattr(self, f'image_{size}'), 'name', filename)
            setattr(self, f'image_{size}_url', filename)

    
    
    if self.image_l.name != self.image_l.field.default:
        # Remove old images
        for size in sizes:
            path = root + getattr(self, f'image_{size}_url')
            try: os.remove(path)
            except: pass

        # Curent admin loaded image path
        try: old_path = image.path
        except: pass

        # Ckeck extantion and make thumbs
        if ext in ['jpg', 'jpeg', 'png', 'gif']:
            make_thumbs(self, image)
        else: pass

        # Remove initial image from temp path
        try: os.remove(old_path)
        except: pass





