from django.db import models


class Note(models.Model):
    header = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='транслит (слаг)',
                            blank=True, null=True)
    content = models.TextField(verbose_name='содержимое заметки')
    preview = models.ImageField(upload_to='notes/', verbose_name='изображение',
                                null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='дата создания')
    is_published = models.BooleanField(default=True,
                                       verbose_name='признак публикации')
    count_view = models.IntegerField(verbose_name='количество просмотров',
                                     default=0)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = ('пост')
        verbose_name_plural = ('посты')
