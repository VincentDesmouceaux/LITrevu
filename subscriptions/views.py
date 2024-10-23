from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured
from .models import UserFollows
from .forms import FollowUserForm

User = get_user_model()

# Vue pour lister les utilisateurs suivis et ceux qui nous suivent


class FollowsListView(LoginRequiredMixin, ListView):
    model = UserFollows
    template_name = 'subscriptions/follow_user.html'
    context_object_name = 'follows'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = UserFollows.objects.filter(user=self.request.user)
        followers = UserFollows.objects.filter(followed_user=self.request.user)
        print(f"DEBUG: Following count: {following.count()}, Followers count: {followers.count()}")
        context['following'] = following
        context['followers'] = followers
        context['form'] = FollowUserForm()  # Ajout du formulaire ici
        print("DEBUG: Formulaire de suivi ajouté au contexte")
        return context

    def get_queryset(self):
        queryset = UserFollows.objects.filter(user=self.request.user)
        print(f"DEBUG: QuerySet pour les utilisateurs suivis récupéré: {queryset}")
        return queryset

# Vue pour ajouter un utilisateur suivi


class FollowUserView(LoginRequiredMixin, FormView):
    form_class = FollowUserForm
    success_url = reverse_lazy('follows_list')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        followed_user = form.cleaned_data['user_id']
        print(f"DEBUG: Tentative de suivre l'utilisateur: {followed_user.username}")
        if followed_user == self.request.user:
            print("DEBUG: Tentative de se suivre soi-même détectée")
            return JsonResponse({"error": "Vous ne pouvez pas vous suivre vous-même."}, status=400)
        if UserFollows.objects.filter(user=self.request.user, followed_user=followed_user).exists():
            print("DEBUG: Cet utilisateur est déjà suivi")
            return JsonResponse({"error": "Vous suivez déjà cet utilisateur."}, status=400)

        # Créer la relation de suivi
        UserFollows.objects.create(user=self.request.user, followed_user=followed_user)
        print(f"DEBUG: Utilisateur {followed_user.username} suivi avec succès")
        return JsonResponse({"success": f"Vous suivez désormais {followed_user.username}."}, status=200)

    def form_invalid(self, form):
        print(f"DEBUG: Le formulaire est invalide - Erreurs: {form.errors}")
        return JsonResponse({"error": "Formulaire invalide."}, status=400)

    def get_template_names(self):
        print("DEBUG: Tentative d'accès à un template dans une vue AJAX")
        raise ImproperlyConfigured(
            "Cette vue est destinée à traiter des requêtes AJAX et ne doit pas rendre de template."
        )

# Vue pour supprimer un utilisateur suivi sans confirmation


class UnfollowUserView(LoginRequiredMixin, DeleteView):
    model = UserFollows
    success_url = reverse_lazy('follows_list')
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        print(f"DEBUG: Tentative de désabonnement de l'utilisateur avec ID: {kwargs['pk']}")
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = UserFollows.objects.filter(user=self.request.user)
        print(f"DEBUG: QuerySet pour les utilisateurs suivis récupéré: {queryset}")
        return queryset

# Vue pour la recherche d'utilisateurs via AJAX pour autocomplétion


class UserSearchView(LoginRequiredMixin, ListView):
    model = User

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        print(f"DEBUG: Requête de recherche reçue avec la requête: '{query}'")
        if query:
            users = User.objects.filter(username__icontains=query)[:5]
            print(f"DEBUG: {users.count()} utilisateurs trouvés pour la requête '{query}'")
            users_data = [{'username': user.username, 'id': user.id} for user in users]  # Inclure l'ID utilisateur
            print(f"DEBUG: Données des utilisateurs retournées: {users_data}")
            return JsonResponse(users_data, safe=False)
        print("DEBUG: Aucune requête de recherche valide, réponse vide retournée")
        return JsonResponse([], safe=False)
