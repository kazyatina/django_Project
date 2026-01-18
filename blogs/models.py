from django.db import models


class Blogs(models.Model):
    title = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Заголовок"
    )
    content = models.TextField(blank=True, null=True, verbose_name="Текст")
    image = models.ImageField(
        upload_to="blogs/images",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publication = models.BooleanField(verbose_name="Признак публикации", default=True)
    views = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
