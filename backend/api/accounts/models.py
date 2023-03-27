from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AccountModel(AbstractBaseUser, PermissionsMixin):
    account = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True) # , primary_key=True == null=False, unique=True
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=255, null=True) # X null=True
    information = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['email', 'name', 'phone'] #, 'company'

    # objects = AccountManager()
    class Meta:
        db_table = 'accounts_table'
    def __str__(self):
        return self.email