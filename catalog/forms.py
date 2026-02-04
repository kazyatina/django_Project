from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, BooleanField, ModelForm

from catalog.models import Product

SPAM_WORDS = [
    "казино",
    "биржа",
    "обман",
    "криптовалюта",
    "дешево",
    "полиция",
    "крипта",
    "бесплатно",
    "радар",
]
class StyleMixin:
    def __init__(self, *args, **kwargs):
        """Стилизация формы."""
        super().__init__(*args, **kwargs)
        # for field_name, field in self.fields.items():
        #     if isinstance(field, BooleanField):
        #         field.widget.attrs['class'] = "form-check-input"
        #     else:
        #         field.widget.attrs['class'] = "form-control"

        # Настройка атрибутов виджета для поля 'name'
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите название",  # Текст подсказки внутри поля
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите описание",  # Текст подсказки внутри поля
            }
        )
        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Прикрепите изображение",  # Текст подсказки внутри поля
            }
        )
        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите цену",  # Текст подсказки внутри поля
            }
        )
        self.fields["category"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите категорию",  # Текст подсказки внутри поля
            }
        )


class ModerationProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ("name", "description")


class ProductsModeratorForm(ModelForm):

    class Meta:
        model = Product
        # отображение колонок
        fields = ("status",)

class ProductForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "price", "category")
        exclude = ("owner",)


    def clean_name(self):
        """Валидация на запрещенные слова в названии."""
        name = self.cleaned_data.get("name")
        if not name:
            raise ValidationError("Поле name не может быть пустым")
        for word in SPAM_WORDS:
            if word in name:
                raise ValidationError(
                    f"Запрещенные слова {word}, которые нельзя использовать в названиях"
                )
        return name

    def clean_description(self):
        """Валидация на запрещенные слова в описании."""
        description = self.cleaned_data.get("description")
        for word in SPAM_WORDS:
            if word in description:
                raise ValidationError(
                    f"Запрещенные слова {word}, которые нельзя использовать в описаниях"
                )
        return description

    # def clean_image(self):
    #     """Валидация названия."""
    #
    #     image = self.cleaned_data.get("image")
    #     max_size = 5 * 1024 * 1024  # 5MB
    #     valid_formats = ["jpeg", "jpg", "png"]
    #     file_extension = image.name.split(".")[-1].lower()  # Получаем расширение файла
    #
    #     if file_extension not in valid_formats:
    #         raise ValidationError(
    #             "Недопустимый формат изображения. Разрешены: .jpeg, .jpg, .png"
    #         )
    #
    #     if image and image.size > max_size:
    #         self.add_error("image", "Размер изображения не должен превышать 5MB.")
    #
    #     # if Product.objects.filter(name=name).exists():
    #     #     raise ValidationError("Продукт с таким названием уже существует")
    #     return image

    def clean_price(self):
        """
        Проверка поля price(цена) на условие > 0
        """
        price = self.cleaned_data.get("price")
        if price and price < 0:
            self.add_error("price", f"Цена не может быть меньше 0")
        return price

    def clean_image_size(self):
        """Валидация размера изображения."""
        image = self.cleaned_data.get("image")
        max_size = 5 * 1024 * 1024  # 5MB
        if image and image.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5MB.")

    def clean_image_format(self):
        """Валидация формата изображения."""
        image = self.cleaned_data.get("image")
        valid_formats = ["jpeg", "jpg", "png"]
        file_extension = image.name.split(".")[-1].lower()  # Получаем расширение файла
        if file_extension not in valid_formats:
            raise ValidationError(
                "Недопустимый формат изображения. Разрешены: .jpeg, .jpg, .png"
            )




class CheckboxForm(StyleMixin, forms.Form):
    my_checkbox = forms.BooleanField(label="Подтверждаю", required=True)
