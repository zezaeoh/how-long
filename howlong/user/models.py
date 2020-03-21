from django.db import models

# Create your models here.
from django.contrib.auth.models import UserManager as DefaultUserManager, User


class UserManager(DefaultUserManager):
    # 페이스북으로 가입하면 user_type을 F(Facebook)으로 지정한다.
    def get_or_create_facebook_user(self, user_pk, extra_data):
        user = User.objects.get(pk=user_pk)
        user.user_type = "F"
        user.save()

        return user

    # 네이버로 가입하면 user_type을 N(Naver)으로 지정한다. 그외에 커스텀 저장을 한다.
    def get_or_create_naver_user(self, user_pk, extra_data):
        user = User.objects.get(pk=user_pk)
        user.username = extra_data['name']
        user.nickname = extra_data['nickname']
        user.email = extra_data['email']
        user.first_name = extra_data['name'][0]
        user.last_name = extra_data['name'][1:]
        user.profile_image = extra_data['profile_image']
        user.user_type = "N"
        user.save()

        return user