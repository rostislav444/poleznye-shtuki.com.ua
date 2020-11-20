from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from apps.user.models import CustomUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def email_validator(value):
    try: 
        validate_email(value)
        return  True
    except:  return 'E-mail Имеет не корреетный форма'

validator = {
    'email' : email_validator
}




class UserViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]
    context = {}
    

    def login(self, request):
        args = self.context 
        args['redirect'] = request.GET.get('redirect')

        if request.method == 'POST':
            last_url = request.META.get('HTTP_REFERER')
            data = request.data
            # FIND USER
            try: user = CustomUser.objects.get(email=data.get('email'))
            except: 
                user = None
                args['msg'] = "Пользователь с таким E-mail не зарегестрирован в системе"
            # TRY PASSWORD
            if user:
                user = authenticate(request, username=user.email, password=data['password'])
                if user is not None:
                    login(request, user)
                    if args['redirect']:
                        return redirect(args['redirect'])
                    else:
                        return redirect('/')
                else:
                    args['msg'] = "Введен не правильный пароль"
        return render(request, 'user/login.html', args)

    def register(self, request):
        errors, args = [], {}
        args['redirect'] = request.GET.get('redirect')
        if request.method == 'POST':
            data=request.data
            args['data']=data
             # EMAIL
            email = data.get('email')
            try: validate_email(data.get('email'))
            except: errors.append('E-mail Имеет не корреетный форма')
            # USER
            user = CustomUser.objects.filter(email=email).first()
            if user: errors.append('Пользователь с таким E-mail уже зарегестрирован')
            # PASSWORD
            password, password2 = data.get('password'), data.get('password2')
            if password:
                if len(password) < 6:
                    errors.append('Пароль слишком короткий')
                if password != password2:
                    errors.append('Пароли не совпадают')
            else:
                errors.append('Введите пароль')
            if len(errors) == 0:
                user = CustomUser(
                    email = data.get('email'),
                    name = data.get('name'),
                    surname = data.get('surname'),
                )
                user.set_password(password)
                user.save()
                login(request, user)
                if args['redirect']:
                    return redirect(args['redirect'])
                else:
                    return redirect('/')
            else:
                args['msg'] = ', '.join(errors)

        return render(request, 'user/register.html', args)
        

    def profile(self, request):
        auth = False
        if auth == False:
            return render(request, 'user/login.html')
        else:
            return redirect('/')