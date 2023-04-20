from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.accounts'
    def ready(self):
        from api.accounts.signals import create_groups, create_default_managers, create_default_engineers




    # def ready(self):
    #     from api.accounts.models import AccountModel
    #     from api.accounts.serializers import AccountSerializer
        
    #     for i in range(1, 11):
    #         if AccountModel.objects.get(account=f"user{i}").exists() == False:
    #             data = {"account": f"user{i}", "email": f"user{i}@gmail.com", "name": f"user{i}", "password": "1234", "phone": "1234"}
    #             serializer = AccountSerializer(data=data)
    #             if serializer.is_valid():
    #                 user = serializer.save()
    #                 user.set_password(user.password)
    #                 user.is_active = True
    #                 user.save()
                



