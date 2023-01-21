# users/management/commands/createsu.py

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not get_user_model().objects.filter(username='admin').exists():
            get_user_model().objects.create_superuser(
                username='admin',
                password='admin',
                email='admin@gmail.com'
            )

        print('Superuser has been created.')
