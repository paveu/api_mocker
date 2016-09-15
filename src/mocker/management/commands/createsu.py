from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
MyUser = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not MyUser.objects.filter(username="admin").exists():
            MyUser.objects.create_superuser(
                "admin",
                "admin@admin.com",
                "admin"
)