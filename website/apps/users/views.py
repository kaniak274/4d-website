from datetime import datetime
import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, ListView, View

from website.apps.common.utils import compose_email
from website.apps.news.use_cases import get_all_news
from website.apps.ranking.use_cases import get_guilds_ranking, get_players_ranking

from .models import User, OK_STATUS
from .forms import CustomPasswordResetForm, RegisterForm


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        errors = json.loads(request.session.get('login_form_error', "{}"))

        if errors:
            del request.session['login_form_error']
            request.session.modified = True

        context = {
            'login_form': AuthenticationForm(request=request),
            'news': get_all_news(),
            'login_errors': errors,
            'player_ranking': get_players_ranking(),
            'guild_ranking': get_guilds_ranking(),
        }

        return render(request, self.template_name, context)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = '/'
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = User.objects.create_user(
            form.cleaned_data['login'],
            form.cleaned_data['email'],
            form.cleaned_data['social_id'],
            form.cleaned_data['password'],
        )

        message_ctx = self._prepare_message_context()

        compose_email(
            [form.cleaned_data['email']],
            subject_tpl='users/email/registration_email.txt',
            msg_tpl='users/email/registration.html',
            subject_ctx=None,
            msg_ctx=message_ctx,
        )

        return HttpResponseRedirect(self.get_success_url())

    def _prepare_message_context(self):
        return {
            'user': self.object,
            'domain': get_current_site(self.request),
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
            'token': default_token_generator.make_token(self.object),
        }


class CustomLoginView(LoginView):
    success_url = '/'
    form_class = AuthenticationForm
    http_method_names = ['post']
    template_name = 'home.html'

    def form_invalid(self, form):
        self.request.session['login_form_error'] = form.errors.as_json()
        return redirect('/')


class BanListView(ListView):
    model = User
    queryset = User.objects.exclude(availDt=datetime(1, 1, 1))
    template_name = 'bans/ban_list.html'
    paginate_by = 20


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.status = OK_STATUS
        user.save()

        return HttpResponse('Twój email został potwierdzony. Teraz możesz zalogować się swoim kontem.')
    else:
        return HttpResponse('Link aktywacyjny jest zły!')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def form_invalid(self, form):
        return super().form_invalid()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['data'] = json.loads(self.request.body)

        return kwargs
