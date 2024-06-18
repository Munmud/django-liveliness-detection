import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

STS_METADATA_CSV = os.path.join(settings.DATA_DIR, "sts.csv")
VEHICLE_METADATA_CSV = os.path.join(settings.DATA_DIR, "vehicle.csv")
NEIGHBOURHOOD_METADATA_CSV = os.path.join(
    settings.DATA_DIR, "neighbourhood.csv")


def create_system_admin(username, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password=password)
        group, created = Group.objects.get_or_create(name='System Admin')
        user.groups.add(group)
        user.is_staff = True
        user.save()
        print(f"User '{username}' is now a system admin.")


def is_system_admin(user):
    return user.groups.filter(name=settings.GROUP_NAME_SYSTEM_ADMIN).exists()


def is_sts_manager(user):
    return user.groups.filter(name=settings.GROUP_NAME_STS_MANAGER).exists()


def is_landfill_manager(user):
    return user.groups.filter(name=settings.GROUP_NAME_LANDFILL_MANAGER).exists()


def is_contractor_manager(user):
    return user.groups.filter(name=settings.GROUP_NAME_CONTRACTOR_MANAGER).exists()


def is_workforce(user):
    return user.groups.filter(name=settings.GROUP_NAME_WORKFORCE).exists()


def is_citizen(user):
    return user.groups.filter(name=settings.GROUP_NAME_CITIZEN).exists()
