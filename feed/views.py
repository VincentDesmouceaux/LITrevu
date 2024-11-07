from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q, Value, CharField
from itertools import chain
from reviews.models import Ticket, Review
from django.contrib.auth.mixins import LoginRequiredMixin

# Page FeedView (flux de tous les utilisateurs)


class FeedView(LoginRequiredMixin, ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')  # Rediriger si non connecté

    def get_queryset(self):
        tickets = Ticket.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all())
        ).annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all()) |
            Q(ticket__user=self.request.user)
        ).annotate(content_type=Value('REVIEW', CharField()))

        # Ajouter un indicateur pour vérifier si l'utilisateur connecté a déjà posté une critique
        for ticket in tickets:
            ticket.has_user_reviewed = reviews.filter(ticket=ticket, user=self.request.user).exists()

        # Fusionner et trier les tickets et critiques
        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        context['rating_range'] = [1, 2, 3, 4, 5]  # Pour afficher les étoiles
        return context

# Page PostView (voir uniquement les propres posts de l'utilisateur connecté)


class PostView(LoginRequiredMixin, ListView):
    template_name = 'feed/posts.html'
    context_object_name = 'user_posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        # Critiques
        reviews = Review.objects.filter(
            Q(user=self.request.user) | Q(ticket__user=self.request.user)
        ).annotate(content_type=Value('REVIEW', CharField())).order_by('-time_created')

        # Tickets
        tickets = Ticket.objects.filter(user=self.request.user).annotate(
            content_type=Value('TICKET', CharField())).order_by('-time_created')

        return {'reviews': reviews, 'tickets': tickets}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = self.get_queryset()
        context['reviews'] = user_posts['reviews']
        context['tickets'] = user_posts['tickets']
        context['rating_range'] = [1, 2, 3, 4, 5]  # Pour afficher les étoiles dynamiquement
        return context
