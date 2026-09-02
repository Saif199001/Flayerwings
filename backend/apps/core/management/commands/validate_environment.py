from django.core.management.base import BaseCommand
from django.core.management import call_command

from apps.core.security import validate_production_settings


class Command(BaseCommand):
    help = "Run Django deployment checks and verify production environment configuration and migration state."

    def handle(self, *args, **options):
        self.stdout.write("Running Django deployment checks...")
        call_command("check", deploy=not self._debug_enabled())
        self.stdout.write(self.style.SUCCESS("Django deployment checks completed."))

        if not self._debug_enabled():
            self.stdout.write("Validating production environment...")
            validate_production_settings()
            self.stdout.write(self.style.SUCCESS("Production environment validation completed."))

        self.stdout.write("Checking migration state...")
        call_command("makemigrations", "--check", "--dry-run", verbosity=1)
        self.stdout.write(self.style.SUCCESS("Migration check completed."))

    @staticmethod
    def _debug_enabled():
        from django.conf import settings
        return settings.DEBUG
