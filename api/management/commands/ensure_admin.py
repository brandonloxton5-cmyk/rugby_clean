import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create or update an admin/superuser from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")
        email = os.environ.get("ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "ADMIN_USERNAME/ADMIN_PASSWORD not set. Skipping ensure_admin."
            ))
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})

        # Ensure flags
        user.is_staff = True
        user.is_superuser = True
        if email:
            user.email = email

        # Always enforce password from env (so you can reset without shell)
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin user '{username}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated admin user '{username}'"))
