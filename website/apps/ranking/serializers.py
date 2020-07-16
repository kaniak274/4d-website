from rest_framework import serializers

from .models import Guild, Player


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = ('guild_name', 'points')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('kills', 'name')
