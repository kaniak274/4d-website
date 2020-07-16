from rest_framework import serializers

from .models import Guild, Player


class GuildSerializer(serializers.ModelSerializer):
    place = serializers.SerializerMethodField()

    class Meta:
        model = Guild
        fields = ('name', 'ladder_point', 'win', 'loss', 'draw', 'place')

    def get_place(self, obj):
        return obj.place


class BasePlayerSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    empire = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()

    def get_job(self, obj):
        return obj.job_to_class

    def get_empire(self, obj):
        return obj.get_empire

    def get_place(self, obj):
        return obj.place


class PlayerSerializer(BasePlayerSerializer):
    class Meta:
        model = Player
        fields = ('kills', 'name', 'job', 'empire', 'place')


class PlayerPlayTimeSerializer(BasePlayerSerializer):
    playtime = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('playtime', 'name', 'job', 'empire', 'place')

    def get_playtime(self, obj):
        return obj.playtime_label
