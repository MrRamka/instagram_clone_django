from django.core.management import BaseCommand
from mixer.backend.django import mixer

from user_profile.models import Profile


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            default=1,
            type=int,
            help=f'Amount of Users'
        )

    def handle(self, *args, **options):
        amount = options['amount']

        for i in range(amount):
            user = mixer.blend(Profile)
            user.save()
