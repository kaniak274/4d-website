from django.db import models


class News(models.Model):
    class Meta:
        db_table = 'site_news'
        verbose_name_plural = 'news'
        ordering = ('-date',)

    topic = models.CharField(max_length=30)
    content = models.TextField()

    date = models.DateTimeField()
    author = models.CharField(max_length=12)
