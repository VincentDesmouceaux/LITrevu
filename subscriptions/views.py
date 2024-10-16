from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.db.models.functions import Substr
from .models import UserFollows
from .forms import FollowUserForm

User = get_user_model()

# Vue pour lister les utilisateurs suivis et ceux qui nous suivent


class FollowsListView(LoginRequiredMixin, ListView):
    model = UserFollows
    template_name = 'subscriptions/follows_list.html'
    context_object_name = 'follows'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Liste des utilisateurs que l'on suit
        following = UserFollows.objects.filter(user=self.request.user)

        # Liste des utilisateurs qui nous suivent
        followers = UserFollows.objects.filter(followed_user=self.request.user)

        # Ajouter les données au contexte
        context['following'] = following
        context['followers'] = followers
        return context

    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)

# Vue pour ajouter un utilisateur suivi


class FollowUserView(LoginRequiredMixin, FormView):
    form_class = FollowUserForm
    template_name = 'subscriptions/follow_user.html'
    success_url = reverse_lazy('follows_list')
    login_url = reverse_lazy('login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial_letter = self.request.GET.get('letter')  # Récupère la lettre initiale si fournie
        kwargs['initial_letter'] = initial_letter
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Extraire les premières lettres des noms d'utilisateurs uniques en base de données
        letters = User.objects.annotate(
            first_letter=Substr('username', 1, 1)
        ).values_list('first_letter', flat=True).distinct().order_by('first_letter')

        # Ajouter les lettres au contexte
        context['letters'] = letters
        return context

    def form_valid(self, form):
        followed_user = form.cleaned_data['username']
        if followed_user == self.request.user:
            # Empêcher de suivre soi-même
            return redirect('follows_list')

        # Empêcher de suivre deux fois le même utilisateur
        if UserFollows.objects.filter(user=self.request.user, followed_user=followed_user).exists():
            return redirect('follows_list')

        # Créer la relation de suivi
        UserFollows.objects.create(user=self.request.user, followed_user=followed_user)
        return super().form_valid(form)

# Vue pour supprimer un utilisateur suivi


class UnfollowUserView(LoginRequiredMixin, DeleteView):
    model = UserFollows
    template_name = 'subscriptions/unfollow_user_confirm.html'
    success_url = reverse_lazy('follows_list')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)
