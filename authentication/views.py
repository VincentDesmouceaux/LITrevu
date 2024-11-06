from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth import login  # Ajout de cet import
from django.shortcuts import redirect  # Pour la redirection
from .models import CustomUser
from .forms import CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('feed')  # Redirection vers la page de flux après connexion réussie

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('feed')

    def form_invalid(self, form):
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        return super().form_invalid(form)

    def form_valid(self, form):
        print("L'utilisateur se connecte...")
        response = super().form_valid(form)
        print(f"Utilisateur connecté : {self.request.user}")
        print(f"Authentifié ? {self.request.user.is_authenticated}")
        return response


class UserLogoutView(LogoutView):
    next_page = 'homepage'


class UserSignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Inscription réussie ! Bienvenue sur LITRevu.")
        return response


class HomePageView(TemplateView):
    template_name = 'authentication/homepage.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirection vers le flux si l'utilisateur est connecté
            return redirect('feed')
        print(f"Utilisateur sur la page d'accueil : {request.user}")
        print(f"Authentifié ? {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)
