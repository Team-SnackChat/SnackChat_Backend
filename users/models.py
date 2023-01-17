from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .utils import rename_imagefile_to_uuid

class UserManager(BaseUserManager):
    def create_user(self, email, nickname ,password=None): 
  
        if not email: 
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None):
   
        user = self.create_user(
            password=password,
            nickname=nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# 사용자모델 
class User(AbstractBaseUser):
    email = models.EmailField("이메일" , max_length=255) 
    nickname = models.CharField("닉네임", max_length=30, unique=True)
    provider = models.CharField(max_length=30)
    # profile_image = models.ImageField(default='/default_profile/default.PNG', upload_to=rename_imagefile_to_uuid)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin