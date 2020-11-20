from django.apps import AppConfig
from django.apps.registry import Apps
from django.db import models
from django.contrib import admin
from django.apps import apps
from django.forms import TextInput, Textarea
import jsonfield
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe




FORMFIELD_OVERRIDES = {
    models.CharField: {'widget': TextInput(attrs={'size':'63'})},
    models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':61})},
    jsonfield.JSONField: {'widget': Textarea(attrs={'rows':2, 'cols':61})},
}

# Class for hidding model in main list
class HiddenModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


def create_model(name,parent_model_name=None,fields=None,inherit=models.Model,app_label=None,module='',options=None,admin_parent=None,admin_opts=None):
    class Meta:
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)
    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (inherit,), attrs)

    # Create an Admin class if admin options were provided
    
    if admin_opts is not None:
        # attrs = {
        #     'formfield_overrides' : FORMFIELD_OVERRIDES,
        #     'model': model,
        #     'extra': 0,
        #     '__module__': 'apps.' + app_label + '.admin',
        #     'sortable_options' : 'parent'
        # }
        admin_model_inline = type(parent_model_name + "TranslationInline", (admin.StackedInline,), {
            'formfield_overrides' : FORMFIELD_OVERRIDES,
            'model': model,
            'extra': 0,
            '__module__': 'apps.' + app_label + '.admin',
            'sortable_options' : 'parent'
        })


        admin_model = type(parent_model_name + "TranslationAdmin", (HiddenModelAdmin,), {
            '__module__': 'apps.' + app_label + '.admin',
            'formfield_overrides' : FORMFIELD_OVERRIDES,
        })

        admin.site.register(model, admin_model)

        # AdminModelOfInline = type(parent_model_name + "TranslationInline", (inherit,), attrs)

        def edit(self, obj=None):
            if obj.pk:
                url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
                url = '<a href="{url}">{text}</a>'.format(url=url,text='Редактировать',)
                return mark_safe(url)
            return _("Нажмите сохранить и продолжить, для получения ссылки редактирования")

        readonly_fields = ['edit']
        fields =  ['edit']

        setattr(admin_model_inline, 'edit', edit)
        setattr(admin_model_inline, 'readonly_fields', readonly_fields)
        setattr(admin_model_inline, 'fields', fields)

        if admin_parent != None:
            if len(admin_parent.inlines) == 0:
                admin_parent.inlines = []
            admin_parent.inlines.append(admin_model_inline)

        for key, value in admin_opts:
            setattr(admin_model_inline, key, value)
    return model




class CoreConfig(AppConfig):
    name = 'apps.core'


    def ready(self):
        from apps.core.models import Language, Translation

        def getModule(app_name=None):
            module = __import__('apps')
            path = app_name + '.admin'
            for directory in path.split('.'):
                module = getattr(module, directory)
            return module


        def RegisterModelAdmin(model, app_name):
            modelName = model.__name__
            admin_model = type(modelName + "Admin", (HiddenModelAdmin,), {
                '__module__': 'apps.' + app_name + '.admin',
                'formfield_overrides' : FORMFIELD_OVERRIDES,
            })

            admin.site.register(model, admin_model)
            return admin_model
        
        
        for model in Translation.__subclasses__():
            if model._meta.proxy == False:
                app_name =  model._meta.app_label
                module = getModule(app_name)
                """
                Get model admin, if it exists, else create and register it.
                """
                if hasattr(module, model.__name__ + 'Admin'):
                    admin_parent = getattr(module, model.__name__ + 'Admin')
                else:
                    admin_parent =  RegisterModelAdmin(model, app_name)
            
                modelName = model.__name__
                translationModelName = model.__name__ + 'Translation'
                
                fields = {
                    'parent' : models.ForeignKey(app_name + '.' + model.__name__, on_delete=models.CASCADE, related_name='translation')
                }

                for field in model._meta.get_fields(include_hidden=False):
                    if field.get_internal_type() in ['CharField', 'TextField'] and 'json' not in str(field.name).lower():
                        fields[field.name] = field
                # OPTIONS
                options = {}
                for option in ['verbose_name', 'verbose_name_plural']:
                    if hasattr(model._meta, option):
                        options[option] = getattr(model._meta, option) + ' (перевод)'
                # CREATE MODEL
                model = create_model(
                    app_label=app_name, 
                    name=translationModelName, 
                    parent_model_name = modelName,
                    inherit=Language, 
                    fields=fields, 
                    options=options, 
                    module=model.__module__, 
                    admin_opts={},
                    admin_parent=admin_parent
                )
            
