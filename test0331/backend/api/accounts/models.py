from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
    def get_by_natural_key(self, account):
        user = self.get(account=account)
        print('Found user:', user)
        return user

class AccountModel(AbstractBaseUser, PermissionsMixin):
    account = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True) # , primary_key=True == null=False, unique=True
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=255, null=True) # XXX null=True
    information = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['email', 'name', 'phone'] #, 'company'

    objects = AccountManager()
    class Meta:
        db_table = 'tap_accounts_table'
    def __str__(self):
        return self.email
