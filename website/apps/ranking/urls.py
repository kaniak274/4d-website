from django.urls import path

from .views import GuildRankingView, PlayerRankingView, RankingView, NolifesRankingView


urlpatterns = [
    path('guild-ranking/', GuildRankingView.as_view(), name='guild-ranking-list'),
    path('player-ranking/', PlayerRankingView.as_view(), name='player-ranking-list'),
    path('nolife-ranking/', NolifesRankingView.as_view(), name='nolife-ranking-list'),
    path('ranking/', RankingView.as_view(), name='ranking'),
]
