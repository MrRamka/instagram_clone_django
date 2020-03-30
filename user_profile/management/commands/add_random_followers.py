import random

from django.core.management import BaseCommand
from mixer.backend.django import mixer

from user_profile.models import Profile


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            default=1,
            type=int,
            help=f'Amount of Followers'
        )

    def handle(self, *args, **options):
        amount = options['amount']

        temp_amount = 0

        users = Profile.objects.all()
        while temp_amount < amount:

            for profile in users:
                add = True if random.randint(0, 1) == 1 else False
                if add:
                    follows = random.choice(users)
                    profile.follows.add(follows)
                    temp_amount += 1
                if temp_amount >= amount:
                    break
