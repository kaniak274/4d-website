from django.core.paginator import Paginator

from .models import Player, Guild


PAGINATE_BY = 10


def get_guilds_ranking():
    all_guilds = Guild.objects.all().order_by('-points')
    paginator = Paginator(all_guilds, PAGINATE_BY)

    return paginator.get_page(1)


def get_players_ranking():
    all_players = Player.objects.all().order_by('-kills')
    paginator = Paginator(all_players, PAGINATE_BY)

    return paginator.get_page(1)
