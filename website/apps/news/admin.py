from django.contrib import admin

from website.apps.common.utils import get_static_url

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date', 'author',)
    search_fields = ('topic', 'author',)

    class Media:
        js = (get_static_url('news_preview', 'js'), get_static_url('runtime', 'js'))


admin.site.register(News, NewsAdmin)
