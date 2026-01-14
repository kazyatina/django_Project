from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(
            name="Новый год", description="украшения"
        )

        products = [
            {
                "name": "Игрушки",
                "description": "на ёлку",
                "image": "",
                "price": 100,
                "created_at": "2025-12-20",
                "updated_at": "2025-12-20",
                "category": category,
            },
            {
                "name": "Гирлянда",
                "description": "на улицу",
                "image": "",
                "price": 100,
                "created_at": "2025-12-20",
                "updated_at": "2025-12-20",
                "category": category,
            },
        ]

        for pro in products:
            product, created = Product.objects.get_or_create(**pro)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Успешно добавлен продукт {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Продукт {product.name} уже существует")
                )
