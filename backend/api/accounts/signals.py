from django.contrib.auth.models import Group, Permission
from api.accounts.models import AccountModel
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from api.accounts.serializers import AccountSerializer
import logging
logger = logging.getLogger(__name__)
# # create groups
# engineer_group = Group.objects.create(name='Engineers')
# supervisor_group = Group.objects.create(name='Supervisiors')


# # assign permissions
# # permission = Permission.objects.get(codename='can_manage')
# # supervisor_group.permissions.add(permission)
# permissions = Permission.objects.filter(codename__in=['can_manage', 'can_delete_engineer'])
# supervisor_group.permissions.set(permissions)


@receiver(post_migrate) # run after migrate 
def create_groups(sender, **kwargs):
    group_name = 'Supervisiors'
    if not Group.objects.filter(name=group_name).exists():
        group = Group.objects.create(name=group_name)
        permissions = Permission.objects.create(
            codename = 'can_manage',
            content_type=ContentType.objects.get_for_model(AccountModel))
        group.permissions.add(permissions)
        logger.info(f'Groups {group_name} created')
    else:
        logger.info(f'Group {group_name} already exists')

    group_name = 'Engineers'
    if not Group.objects.filter(name=group_name).exists():
        Group.objects.create(name=group_name)
        logger.info(f'Groups {group_name} created')
    else:
        logger.info(f'Group {group_name} already exists')



@receiver(post_migrate)
def create_default_engineers(sender, **kwargs):
    group = Group.objects.get(name='Engineers')
    for i in range(0, 11):
        data = {"account": f"user{i}", "email": f"user{i}@gmail.com", "name": f"user{i}", "password": "1234", "phone": "1234"}
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.is_active = True
            group.user_set.add(user)
            user.save()

@receiver(post_migrate)
def create_default_managers(sender, **kwargs):
    group = Group.objects.get(name='Supervisiors')
    for i in range(1, 11):
        data = {"account": f"manager{i}", "email": f"manager{i}@gmail.com", "name": f"manager{i}", "password": "1234", "phone": "1234"}
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.is_active = True
            group.user_set.add(user)
            user.save()



# class Group():
#     def _create_group():
#         # assign permissions
#         # permission = Permission.objects.get(codename='can_manage')
#         # supervisor_group.permissions.add(permission)
#         permissions = Permission.objects.filter(codename__in=['can_manage', 'can_delete_engineer'])
#         supervisor_group.permissions.set(permissions)
#     def add_user_to_group(account):
#         # add user to group
#         user  = AccountModel.objects.get(account=account)
#         user.gr
#         engineer_group.user_set.add(user)
#         user = AccountModel.objects.create_user(account=account, password='')


# def view(request):
#     user
#     if not user.groups.filter(name='supervisiors').exists():
#         not have access
#         return  
    

# def view(resuet):
#     if not user.has_perm('app_label.can_manage ')

