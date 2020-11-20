from django.db import models
from googletrans import Translator
from textblob import TextBlob
from project import settings
from django.utils.translation import get_language as lang
from django.apps import apps
from bs4 import BeautifulSoup
from translate import Translate
import requests


class Languages(models.Model):
    code =  models.CharField(max_length=10,  unique=True, choices=settings.LANGUAGES)
    name =  models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
   

    class Meta:
        verbose_name = 'Активный язык'
        verbose_name_plural = 'Активные языки'

    def __str__(self):
        return self.code + ' - ' + self.name

    def save(self):
        self.name = dict(settings.LANGUAGES)[self.code]
        super(self.__class__, self).save()


def TranslatorsTranslate(text, language, ignore=True):
    if language == 'ru' and ignore == True: 
        translation = text
    else:
        try:
            blob = TextBlob(text)
            translation = blob.translate(to=language)
        except: 
            try:
                translator = Translator()
                translation = translator.translate(text, dest=language).text
            except: translation = text
    return str(models.Model)




def trans():
    url = "https://sa-translate.p.rapidapi.com/translate"

    payload = {
        "text": "Provide some text you would like to translate into another language",
        "targetLanguage": "pt"
    }
    headers = {
        'x-rapidapi-host': "sa-translate.p.rapidapi.com",
        'x-rapidapi-key': "83384569fcmsh117d739d038bcb5p1d350fjsndf37de4019b4",
        'content-type': "application/json",
        'accept': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)




class Language(models.Model):
    translate = models.BooleanField(default=True, verbose_name="Перевести")
    language =  models.ForeignKey('core.Languages', blank=False, on_delete=models.CASCADE, verbose_name="Язык")
    
    class Meta:
        abstract = True

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __str__(self):
        return str(self.language.code)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

       
    def save(self):
        translate_childs = False
       
        if self.translate == True:
            trans()
            translator = Translator()
            for field in self.parent._meta.get_fields():
                if field.get_internal_type() in ['CharField','TextField']:
                    text = getattr(self.parent, field.name)
                    # if field.__module__ == "ckeditor.fields":
                    #    pass
                    if text != None:
                        if len(text) > 0:
                            
                            translation = TranslatorsTranslate(text, self.language.code)
                            setattr(self, field.name, translation)
                        else:
                            setattr(self, field.name, '')
                    else:
                        setattr(self, field.name, '')
                # self.translate = False

            try:
                self.slug = slugify(str(unidecode.unidecode(self.parent.slug + '-' + str(self.language.code))))
            except: pass
        self.translate = False
        super(Language, self).save()





# ABSTRACT
class Translation(models.Model):
    translate_childs = models.BooleanField(default=False, verbose_name='Перевод')

    class Meta:
        abstract = True

    def translate(self):
        current_language = lang()
        if settings.LANGUAGE_CODE != current_language:
            try: return self.translation.get(language__code=lang())
            except: return self
        else: return self


    def save(self):
        super(Translation, self).save()
        ModelTranslation = apps.get_model(self._meta.app_label, self._meta.model_name +'Translation')
        # TRANSLATE
        for language in Languages.objects.all():
            if language.code != settings.LANGUAGE_CODE:
                try:    child = ModelTranslation.objects.get(parent=self, language=language)
                except: child = ModelTranslation(parent=self, language=language)
                child.translate = True
                child.save()
