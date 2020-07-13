from django.views.generic import CreateView, View
from django.shortcuts import render

from .models import User
from .forms import RegisterForm


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = '/'
    template_name = 'users/register.html'

    def form_valid(self, form):
        ### TODO Send email.
        return super().form_valid(form)
