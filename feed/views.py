from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q, Value, CharField
from itertools import chain
from reviews.models import Ticket, Review
from django.contrib.auth.mixins import LoginRequiredMixin

# View principale pour le flux de tous les utilisateurs


class FeedView(LoginRequiredMixin, ListView):
    """
    Vue pour afficher le flux des posts de l'utilisateur courant et de ceux qu'il suit.
    Seuls les utilisateurs connectés peuvent accéder à cette vue.

    Attributes:
        template_name (str): Template HTML utilisé pour le rendu du flux.
        context_object_name (str): Nom de l'objet contextuel contenant les posts.
        login_url (str): URL de redirection si l'utilisateur n'est pas authentifié.
    """
    template_name = 'feed/feed.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')  # Redirige si non connecté

    def get_queryset(self):
        """
        Récupère les tickets et critiques associés à l'utilisateur courant et aux utilisateurs qu'il suit.

        Returns:
            list: Liste triée de tickets et critiques, annotés avec un type de contenu.
        """
        tickets = Ticket.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all())
        ).annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all()) |
            Q(ticket__user=self.request.user)
        ).annotate(content_type=Value('REVIEW', CharField()))

        # Vérifie si l'utilisateur a déjà posté une critique pour chaque ticket
        for ticket in tickets:
            ticket.has_user_reviewed = reviews.filter(ticket=ticket, user=self.request.user).exists()
        for review in reviews:
            review.has_user_reviewed = reviews.filter(ticket=review.ticket, user=self.request.user).exists()

        # Fusionne et trie les tickets et critiques par date de création
        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        return posts

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires au contexte, notamment pour l'affichage des étoiles.

        Returns:
            dict: Contexte enrichi des données nécessaires au rendu du template.
        """
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        context['rating_range'] = [1, 2, 3, 4, 5]  # Pour afficher les étoiles dynamiquement
        return context

# Vue pour voir uniquement les posts de l'utilisateur connecté


class PostView(LoginRequiredMixin, ListView):
    """
    Vue pour afficher uniquement les posts de l'utilisateur connecté.
    Accessible uniquement aux utilisateurs authentifiés.

    Attributes:
        template_name (str): Template HTML pour le rendu de la page "Vos posts".
        context_object_name (str): Nom de l'objet contextuel contenant les posts de l'utilisateur.
        login_url (str): URL de redirection pour les utilisateurs non authentifiés.
    """
    template_name = 'feed/posts.html'
    context_object_name = 'user_posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        """
        Récupère les critiques et tickets créés par l'utilisateur connecté.

        Returns:
            dict: Dictionnaire contenant les critiques et tickets de l'utilisateur, avec type de contenu annoté.
        """
        reviews = Review.objects.filter(
            Q(user=self.request.user) | Q(ticket__user=self.request.user)
        ).annotate(content_type=Value('REVIEW', CharField())).order_by('-time_created')

        tickets = Ticket.objects.filter(user=self.request.user).annotate(
            content_type=Value('TICKET', CharField())).order_by('-time_created')

        return {'reviews': reviews, 'tickets': tickets}

    def get_context_data(self, **kwargs):
        """
        Ajoute des données spécifiques au contexte, comme la plage d'étoiles pour les critiques.

        Returns:
            dict: Contexte avec les critiques, tickets et la plage d'étoiles.
        """
        context = super().get_context_data(**kwargs)
        user_posts = self.get_queryset()
        context['reviews'] = user_posts['reviews']
        context['tickets'] = user_posts['tickets']
        context['rating_range'] = [1, 2, 3, 4, 5]  # Pour afficher les étoiles dynamiquement
        return context
