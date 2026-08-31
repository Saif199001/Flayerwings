from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run Django system checks and verify migration state."

    def handle(self, *args, **options):
        self.stdout.write("Running Django system checks...")
        call_command("check", deploy=not self._debug_enabled())
        self.stdout.write(self.style.SUCCESS("Django checks completed."))

        self.stdout.write("Checking migration state...")
        call_command("makemigrations", "--check", "--dry-run", verbosity=1)
        self.stdout.write(self.style.SUCCESS("Migration check completed."))

    @staticmethod
    def _debug_enabled():
        from django.conf import settings
        return settings.DEBUG
