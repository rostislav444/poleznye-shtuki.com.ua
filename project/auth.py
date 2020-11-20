from apps.user.models import CustomUser
from apps.core.functions.functions__validators import checkPhone, checkEmail



class UserAuthentication(object):
    def authenticate(self, request, username=None, password=None):
        user = CustomUser.objects.filter(email=username).first()
        if user:
            if user.check_password(password):
                return user
            return None
        else:
            return None


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
