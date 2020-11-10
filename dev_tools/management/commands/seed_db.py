from django.core.management.base import BaseCommand, CommandError

from ._db_seeder import seed_all_default


class Command(BaseCommand):
    help = "Seeds the db with dummy data."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        seed_all_default()
