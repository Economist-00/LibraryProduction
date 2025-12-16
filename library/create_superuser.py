import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
user_type = os.environ.get("DJANGO_SUPERUSER_USER_TYPE", "librarian")

if not username or not password:
    raise RuntimeError("Missing DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD")

valid_types = {"employee", "librarian"}
if user_type not in valid_types:
    raise RuntimeError(f"DJANGO_SUPERUSER_USER_TYPE must be one of {valid_types}")

# Create only if it doesn't exist
if not User.objects.filter(username=username).exists():
    u = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    # Ensure required custom field is set
    u.user_type = user_type
    u.save(update_fields=["user_type"])
    print("Superuser created.")
else:
    print("Superuser already exists.")
