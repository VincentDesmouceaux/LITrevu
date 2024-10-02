from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .models import CustomUser
from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True  # Si l'utilisateur est déjà connecté, le rediriger
    success_url = reverse_lazy('homepage')  # Redirection après connexion

    def form_valid(self, form):
        print("L'utilisateur se connecte...")
        response = super().form_valid(form)
        print(f"Utilisateur connecté : {self.request.user}")
        print(f"Authentifié ? {self.request.user.is_authenticated}")
        return response


class UserLogoutView(LogoutView):
    next_page = 'homepage'  # Redirige vers la page d'accueil après la déconnexion


class UserSignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
