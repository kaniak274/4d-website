from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView, ListView, View

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
        ### TODO Send email.
        return super().form_valid(form)


class CustomLoginView(LoginView):
    success_url = '/'
    form_class = AuthenticationForm
    http_method_names = ['post']


class BanListView(ListView):
    model = User
    queryset = User.objects.filter(banlength__isnull=False)
    template_name = 'bans/ban_list.html'
    paginate_by = 20
