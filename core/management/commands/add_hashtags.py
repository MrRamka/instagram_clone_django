from django.core.management import BaseCommand
from mixer.backend.django import mixer

from core.models import HashTag, Place


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--amount',
            default=1,
            type=int,
            help=f'Amount of HashTags'
        )

    def handle(self, *args, **options):
        amount = options['amount']

        for i in range(amount):
            user = mixer.blend(HashTag)
            user.save()
