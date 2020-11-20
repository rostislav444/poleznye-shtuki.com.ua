# DAJNGO
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from apps.core.functions.functions__validators import checkPhone, checkEmail, check_phone_email, validation_response
import urllib.request
import urllib.parse
import uuid
import copy 


def check_user_exists(email=None, phone=None):
    response = {'status' : True, 'data' : None, 'msg' : [],}
    if email != None:
        if len(CustomUser.objects.filter(email=email)) > 0:
            response['status'] = False
            response['msg'].append('Пользователь с таким Email уже существует.') 
            return response
    elif phone != None:
        if len(CustomUser.objects.filter(phone=phone)) > 0:
            response['status'] = False
            response['msg'].append('Пользователь с таким номером телефона уже существует.')
            return response
    return response





class CustomUserManager(BaseUserManager):
    def create_user(self, username, data={}, password=None, request=None):
        msgs = []
        email, phone = check_phone_email(username)
        # If email or phone exists in valid formsts
        if all(var is None for var in [email, phone]):
            msgs.append('Введите корректный номер Телефона или Email')
            return ' '.join(msgs)
        # If uses exists with this formsts
        user_exists = check_user_exists(email=email, phone=phone)
        # print(user_exists)
        if user_exists['status'] == False:
            msgs += user_exists['msg']
            return ' '.join(msgs)

        if len(msgs) > 0:
            return ' '.join(msgs)
            
        user = self.model(
            username = uuid.uuid4(),
            email = email,
            phone = phone,
            name = data['name'] if 'name' in data.keys() else None,
            surname = data['surname'] if 'surname' in data.keys() else None,
        )

        if password != None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    


    def create_superuser(self, username, password, email=None, phone=None):
        user = self.create_user(
            username=username, password=password,
        )
        if isinstance(user, CustomUser) == False:
            raise ValueError(user)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email =    models.EmailField(max_length=255, blank=True, null=True, unique=True, verbose_name="E-mail")
    phone =    models.CharField(max_length=15, blank=True, null=True, unique=True, verbose_name="Телефон")
    name =        models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    surname =     models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")
    patronymic =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Отчество")
    is_active =   models.BooleanField(default=True)
    is_admin =    models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        if self.name and self.surname:
            return ' '.join([self.name, self.surname])
        elif self.name: 
            return self.name
        else:
            return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self,*args,**kwargs):
        # self.phone = checkPhone(self.phone)
        super(CustomUser, self).save(*args,**kwargs)

