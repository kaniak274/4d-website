from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Guild, Player
from .serializers import GuildSerializer, PlayerSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10


class PlayerRankingView(ListAPIView):
    model = Player
    queryset = Player.objects.all().order_by('-kills')
    pagination_class = CustomPagination
    serializer_class = PlayerSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GuildRankingView(ListAPIView):
    model = Guild
    queryset = Guild.objects.all().order_by('-points')
    pagination_class = CustomPagination
    serializer_class = GuildSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['guild_name']
