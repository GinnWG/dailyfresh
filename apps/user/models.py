from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
from dailyfresh import settings

class User(AbstractUser, BaseModel):
    """User Model Class"""

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    """Address Model Manager Class"""

    # 1. change the result set of the original query: all()
    # 2. encapsulate the method: user manipulates the data
    # table corresponding to the model class (add, delete, check and change)

    def get_default_address(self, user):
        # Get the user's default shipping address
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            address = None  # No default address exists

        return address


class Address(BaseModel):
    """Address Model Class"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user')
    receiver = models.CharField(max_length=20, verbose_name='receiver')
    addr = models.CharField(max_length=256, verbose_name='address')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='zip-code')
    phone = models.CharField(max_length=11, verbose_name='phone')
    is_default = models.BooleanField(default=False, verbose_name='is_default')

    # Customize a model manager class
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
