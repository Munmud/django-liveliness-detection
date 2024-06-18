
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from core.utils import create_system_admin

USER_USER1 = 'user1'
USER_USER2 = 'user2'
USER_ADMIN = 'admin'
PASSWORD = 'pass'


def create_general_users(self):
    users_data = [
        {'username': USER_USER1, 'password': PASSWORD},
        {'username': USER_USER2, 'password': PASSWORD},
    ]
    for data in users_data:
        username = data['username']
        password = data['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created user: {username} password: {password}'))
        else:
            self.stdout.write(self.style.WARNING(
                f'User {username} already exists. Skipping...'))

    return [USER_USER1, USER_USER2]


def create_super_user(self):
    username = USER_ADMIN
    password = PASSWORD

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'Superuser\n\t email:\t\t {username}\n\t password:\t {password}'))
    else:
        self.stdout.write(self.style.WARNING(
            f'User {username} already exists. Skipping...'))
    # user, _ = User.objects.get_or_create(username=username, password=password)
    # return user


class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **kwargs):
        create_super_user(self)
        # create_system_admin(
        #     username=USER_ADMIN,
        #     password=PASSWORD,
        # )
        # create_general_users(self)
