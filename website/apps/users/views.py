from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, ListView, View

from website.apps.common.utils import compose_email
from website.apps.news.use_cases import get_all_news

from .models import User
from .forms import RegisterForm


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        context = {
            'login_form': AuthenticationForm(request=request),
            'news': get_all_news(),
        }

        return render(request, self.template_name, context)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = '/'
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        message_ctx = self._prepare_message_context()

        compose_email(
            [form.cleaned_data['email']],
            subject_tpl='users/email/registration_email.txt',
            msg_tpl='users/email/registration.html',
            subject_ctx=None,
            msg_ctx=message_ctx,
        )

        return response

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


class BanListView(ListView):
    model = User
    queryset = User.objects.filter(banlength__isnull=False)
    template_name = 'bans/ban_list.html'
    paginate_by = 20


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        return HttpResponse('Twój email został potwierdzony. Teraz możesz zalogować się swoim kontem.')
    else:
        return HttpResponse('Link aktywacyjny jest zły!')
