from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
# import uuid

# from django.contrib.auth.models import BaseUserManager
# class AccountManager(BaseUserManager):
#     def create_user():
    
#     def create_superuser():

    # password = models.CharField(_("password"), max_length=128)
    # last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    # is_active = True

    # is_superuser = models.BooleanField()
    # groups = models.ManyToManyField()
    # user_permissions = models.ManyToManyField()

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
        db_table = 'account_table'
    def __str__(self):
        return self.email




# class AccountProfileModel(models.Model):
#     account = models.OneToOneField(AccountModel, on_delete=models.CASCADE, primary_key=True)
#     account_name =models.CharField(max_length=100)
#     account_phone = models.CharField(max_length=100)
#     account_information = models.CharField(max_length=200)
#     class Meta:
#         db_table = 'account_profile'
#     def __str__(self):
#         return self.account.email
    

