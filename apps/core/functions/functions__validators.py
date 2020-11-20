import os
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from phonenumber_field.phonenumber import PhoneNumber
from email_validator import validate_email, EmailNotValidError
from django.contrib.gis.geoip2 import GeoIP2
import re

validation_response = {'status' : False,'data' : None,'msg' : [],}


def validateXlsx(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Загрузите таблицу EXCEL в формате .xlsx')


def validateRar(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.rar']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Загрузите архив в формате .rar')


def checkPhone(phone, request=None, country_code='UA'):
    response = validation_response
    phone = re.sub("\D", "", phone)
    if len(phone) < 9:
        response['msg'].append('Номер телефона слишком короткий')
        return response
    elif len(phone) > 15:
        response['msg'].append('Номер телефона слишком длиный')
    if request != None:
        try:
            g = GeoIP2()
            ip = request.META['REMOTE_ADDR']
            country_code = g.country(ip)['country_code']
        except: pass
    try:
        phone = str(PhoneNumber.from_string(phone_number=phone, region=country_code).as_e164).replace('+','')
        response['status'] = True
        response['data'] = phone
        
    except: 
        response['status'] = False
        response['msg'].append('Номер телефона имеет не верный формат')
    return response


def checkEmail(email):
    response = validation_response
    try: 
        validate_email(email, allow_smtputf8=False)
        response['status'] = True
        response['data'] = email
        return response
    except: 
        response['status'] = False
        response['msg'].append('Email имеет не верный формат, либо Вы ввели не существующий домен.')
        return response


def check_phone_email(username, request=None):
    email = None
    phone = None
    # Validate email
    email_valid = checkEmail(username)
    if email_valid['status']:
        email = email_valid['data']
    # Validate phone if not email
    if email == None:
        phone_valid = checkPhone(username, request)
        if phone_valid['status']:
            phone = phone_valid['data']
    return email, phone