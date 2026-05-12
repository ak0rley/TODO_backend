import environ
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

# Initialize environ
env = environ.Env()

# Read .env file
environ.Env.read_env()

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates or updates a superuser using credentials from .env'

    def handle(self, *args, **options):

        # ── Step 1: Read credentials from environment ─────────────────────────
        username = env('ADMIN_USERNAME', default=None)
        email = env('ADMIN_EMAIL', default=None)
        password = env('ADMIN_PASSWORD', default=None)

        # ── Step 2: Validate credentials ──────────────────────────────────────
        if not username or not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    'Missing credentials. Make sure ADMIN_USERNAME, '
                    'ADMIN_EMAIL, and ADMIN_PASSWORD are set in your .env file.'
                )
            )
            return

        # ── Step 3: Check for existing superuser ──────────────────────────────
        existing_user = User.objects.filter(
            Q(username=username) | Q(email=email),
            is_superuser=True
        ).first()


        if existing_user:
            existing_user.set_password(password)
            existing_user.save()

            self.stdout.write(
                self.style.WARNING(
                    f'Superuser "{existing_user.username}" already exists. '
                    'Password updated.'
                )
            )

        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" created successfully.'
                )
            )