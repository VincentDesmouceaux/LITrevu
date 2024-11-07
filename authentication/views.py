from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import CustomUser
from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
    """
    Vue pour la connexion utilisateur.

    Attributs:
        template_name (str): Chemin du template pour la connexion.
        redirect_authenticated_user (bool): Si vrai, redirige les utilisateurs connectés.
        success_url (str): URL de redirection après une connexion réussie.
    """

    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('feed')

    def get_success_url(self):
        """Détermine l'URL de redirection après connexion."""
        return self.get_redirect_url() or reverse_lazy('feed')

    def form_invalid(self, form):
        """Affiche un message d'erreur si le formulaire est invalide."""
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        return super().form_invalid(form)

    def form_valid(self, form):
        """Affiche des informations de débogage après une connexion réussie."""
        response = super().form_valid(form)
        print(f"Utilisateur connecté : {self.request.user}")
        print(f"Authentifié ? {self.request.user.is_authenticated}")
        return response


class UserLogoutView(LogoutView):
    """
    Vue pour la déconnexion utilisateur.

    Attributs:
        next_page (str): Redirige vers la page d'accueil après déconnexion.
    """
    next_page = 'homepage'


class UserSignUpView(CreateView):
    """
    Vue pour l'inscription utilisateur.

    Attributs:
        model (Model): Modèle utilisateur personnalisé.
        form_class (Form): Formulaire d'inscription.
        template_name (str): Chemin du template d'inscription.
        success_url (str): URL de redirection après une inscription réussie.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        """Enregistre et connecte un nouvel utilisateur après une inscription valide."""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Inscription réussie ! Bienvenue sur LITRevu.")
        return response


class HomePageView(TemplateView):
    """
    Vue pour la page d'accueil.

    Attributs:
        template_name (str): Chemin du template pour la page d'accueil.
    """

    template_name = 'authentication/homepage.html'

    def get(self, request, *args, **kwargs):
        """Redirige les utilisateurs connectés vers la page de flux."""
        if request.user.is_authenticated:
            return redirect('feed')
        return super().get(request, *args, **kwargs)
