from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

class EmailBackend(BaseBackend):
    def authenticate(self,request,email=None,passsword=None,**kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            
            if user.check_password(passsword):
                return user
        except UserModel.DoesNotExist:
            return None
    def get_user(self,user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None