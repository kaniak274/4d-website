from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include('website.apps.users.urls')),
    path('', include('website.apps.ranking.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
