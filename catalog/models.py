from django.db import models

from django.db import models

'''Product:
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
'''


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название', unique=True)
    description = models.CharField(max_length=150, verbose_name='Описание')

    def __str__(self):
        """Определяет строковое представление объекта"""
        return f'{self.name}, {self.description}'

    def Meta(self):
        """Используется для добавления метаданных к модели. Он определяет такие свойства, как порядок сортировки,
        наименование модели в единственном и множественном числе и другие"""
        # verbose_name определяют отображаемое имя модели в единственном и множественном числе
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # ordering определяет порядок сортировки объектов при выборке из базы данных
        ordering = ['name']
        # db_table указывает имя таблицы в базе данных, к которой привязана модель
        db_table = 'django_project'

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название', unique=True) # поле для хранения строк
    description = models.TextField(verbose_name='Описание', null=True, blank=True) # поле для хранения больших текстов
    image = models.ImageField(verbose_name='Изображение', upload_to='images/',null=True, blank=True) # поле для хранения информации о загруженных изображениях
    price = models.IntegerField(verbose_name='Цена за покупку') # поле для хранения целых чисел
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата последнего изменения', auto_now=True)

    FOOD = 'food'
    CHEMICAL = 'chemical'
    PETS = 'pet'
    LIST_CHOOSES = [
        (FOOD, 'еда'),
        (CHEMICAL, 'бытовая химия'),
        (PETS, 'для питомцев'),
    ]
    category = models.ForeignKey(Category, choices=LIST_CHOOSES, on_delete=models.CASCADE) # поле для создания внешнего ключа на другую модель

    def __str__(self):
        """Определяет строковое представление объекта"""
        return f'{self.name} - {self.price}, {self.description}'

    def Meta(self):
        """Используется для добавления метаданных к модели. Он определяет такие свойства, как порядок сортировки,
        наименование модели в единственном и множественном числе и другие"""
        # verbose_name определяют отображаемое имя модели в единственном и множественном числе
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        # ordering определяет порядок сортировки объектов при выборке из базы данных
        ordering = ['name']
        # db_table указывает имя таблицы в базе данных, к которой привязана модель
        db_table = 'django_project'
