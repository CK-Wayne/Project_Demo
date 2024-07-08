from django.core.management.base import BaseCommand
from scoreapp.models import User, Item

class Command(BaseCommand):
    help = 'Clears all data from User and Item tables'

    def handle(self, *args, **options):
        User.objects.all().delete()
        Item.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared User and Item tables.'))