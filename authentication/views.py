from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True  # Si l'utilisateur est déjà connecté, le rediriger
    success_url = reverse_lazy('feed')  # Redirection vers la page de flux après connexion réussie

    def get_success_url(self):
        # Gérer la redirection après connexion
        return self.get_redirect_url() or reverse_lazy('feed')

    def form_invalid(self, form):
        # En cas d'échec de connexion, afficher un message d'erreur
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        return super().form_invalid(form)

    def form_valid(self, form):
        # Valider la connexion et afficher des informations sur l'utilisateur connecté
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
    success_url = reverse_lazy('feed')  # Redirection vers la page de flux après l'inscription

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Inscription réussie ! Bienvenue sur LITRevu.")
        return response


class HomePageView(TemplateView):
    template_name = 'authentication/homepage.html'

    def get(self, request, *args, **kwargs):
        # Affichage des informations sur l'utilisateur sur la page d'accueil
        print(f"Utilisateur sur la page d'accueil : {request.user}")
        print(f"Authentifié ? {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)
