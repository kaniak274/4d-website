from django.views.generic import View
from django.shortcuts import render

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Guild, Player
from .serializers import GuildSerializer, PlayerSerializer, PlayerPlayTimeSerializer
from .use_cases import get_guilds_ranking, get_players_ranking, get_nolifes_ranking


class CustomPagination(PageNumberPagination):
    page_size = 1


class PlayerRankingView(ListAPIView):
    model = Player
    queryset = Player.objects.all().order_by('-kills')
    pagination_class = CustomPagination
    serializer_class = PlayerSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class NolifesRankingView(ListAPIView):
    model = Player
    queryset = Player.objects.all().order_by('-playtime')
    pagination_class = CustomPagination
    serializer_class = PlayerPlayTimeSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GuildRankingView(ListAPIView):
    model = Guild
    queryset = Guild.objects.all().order_by('-ladder_point')
    pagination_class = CustomPagination
    serializer_class = GuildSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class RankingView(View):
    template_name = 'ranking/index.html'

    def get(self, request):
        ctx = {
            'player_ranking': get_players_ranking(),
            'guild_ranking': get_guilds_ranking(),
            'nolifes_ranking': get_nolifes_ranking(),
        }

        return render(request, self.template_name, ctx)
