from django.urls import path

from .views import GuildRankingView, PlayerRankingView


urlpatterns = [
    path('guild-ranking/', GuildRankingView.as_view(), name='guild-ranking-list'),
    path('player-ranking/', PlayerRankingView.as_view(), name='player-ranking-list'),
]
