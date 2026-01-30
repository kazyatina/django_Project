from django.db import models

from users.models import CustomUser

"""Product:
наименование,
описание,
изображение,
категория,
цена за покупку,
дата создания,
дата последнего изменения.

Category:
наименование,
описание.
"""


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название", unique=True)
    description = models.CharField(max_length=150, verbose_name="Описание")

    def __str__(self):
        """Определяет строковое представление объекта"""
        return f"{self.name}, {self.description}"

    class Meta:
        """Используется для добавления метаданных к модели. Он определяет такие свойства, как порядок сортировки,
        наименование модели в единственном и множественном числе и другие"""

        # verbose_name определяют отображаемое имя модели в единственном и множественном числе
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Название", unique=True
    )  # поле для хранения строк
    description = models.TextField(
        verbose_name="Описание", null=True, blank=True
    )  # поле для хранения больших текстов
    image = models.ImageField(
        verbose_name="Изображение", upload_to="product/image", null=True, blank=True
    )  # поле для хранения информации о загруженных изображениях
    price = models.IntegerField(
        verbose_name="Цена за покупку"
    )  # поле для хранения целых чисел
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения", auto_now=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )  # поле для создания внешнего ключа на другую модель
    owner = models.ForeignKey(CustomUser, verbose_name='Владелец', blank=True, null=True, help_text='Введите владельца', on_delete=models.CASCADE)

    PUBLIC_STATUS = [
        ('public', 'Опубликовано'),
        ('unpublic', 'Не опубликовано')
    ]
    status = models.CharField(
        max_length=20,
        choices=PUBLIC_STATUS,
        default='unpublic',
        verbose_name='Статус публикации'
    )

    def __str__(self):
        """Определяет строковое представление объекта"""
        return f"{self.name} - {self.price}, {self.description}, {self.category}"

    class Meta:
        """Используется для добавления метаданных к модели. Он определяет такие свойства, как порядок сортировки,
        наименование модели в единственном и множественном числе и другие"""

        # verbose_name определяют отображаемое имя модели в единственном и множественном числе
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        # ordering определяет порядок сортировки объектов при выборке из базы данных
        ordering = ["name"]
        # db_table указывает имя таблицы в базе данных, к которой привязана модель
        # db_table = "django_project"
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
        ]
