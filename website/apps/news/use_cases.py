from .models import News


def get_all_news(page=1):
    ### TODO Pagination
    return News.objects.all()
