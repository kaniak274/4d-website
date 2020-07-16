from django.contrib import admin

from .models import Guild, Player, PlayerIndex

admin.site.register(Guild)
admin.site.register(Player)
admin.site.register(PlayerIndex)
