from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, LogoutView
)

from django.urls import path

from .views import (activate, BanListView, CustomLoginView, HomeView,
    CustomPasswordChangeView, CustomPasswordResetView, RegisterView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('bans/', BanListView.as_view(), name='ban_list'),
    path('activate-email/<str:uidb64>/<str:token>/', activate, name='activate'),

    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password-reset/confirm/<str:uidb64>/<str:token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
