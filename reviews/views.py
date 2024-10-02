from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from users.models import CustomUser  # Mise à jour de l'import
from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    template_name = 'logout.html'


class UserSignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


# Page d'accueil en tant que classe avec TemplateView
class HomePageView(TemplateView):
    template_name = 'homepage.html'
