from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создание группы и назначение прав.'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            permission_unpub = Permission.objects.get(codename='can_unpublish_product')
            permission_del = Permission.objects.get(codename='can_delete_product')
            group.permissions.add(permission_unpub, permission_del)
            self.stdout.write(self.style.SUCCESS('Группа создана, права добавлены.'))
        else:
            self.stdout.write(self.style.WARNING('Группа уже существует.'))
