from django.contrib import admin

from website.apps.common.utils import get_static_url

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date', 'author',)
    search_fields = ('topic', 'author',)

    class Media:
        js = ('/static/news_preview.js', '/static/runtime.js')


admin.site.register(News, NewsAdmin)
