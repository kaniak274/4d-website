from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import activate, BanListView, CustomLoginView, HomeView, RegisterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('bans/', BanListView.as_view(), name='ban_list'),
    path('activate-email/<str:uidb64>/<str:token>/', activate, name='activate'),
]
