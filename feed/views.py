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
        # Billets créés par l'utilisateur ou par les utilisateurs qu'il suit
        tickets = Ticket.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all())  # Correction : utilisation de __in
        ).annotate(content_type=Value('TICKET', CharField()))

        # Critiques créées par l'utilisateur, les utilisateurs qu'il suit, ou en réponse à ses billets
        reviews = Review.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all()) |  # Correction : utilisation de __in
            Q(ticket__user=self.request.user)
        ).annotate(content_type=Value('REVIEW', CharField()))

        # Bloquer la création de critiques pour les billets déjà commentés par l'utilisateur
        for ticket in tickets:
            ticket.has_user_reviewed = reviews.filter(ticket=ticket, user=self.request.user).exists()

        # Combiner et trier les billets et les critiques par ordre antéchronologique
        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        return context


# Page PostView (voir uniquement les propres posts de l'utilisateur connecté)
class PostView(LoginRequiredMixin, ListView):
    template_name = 'feed/posts.html'  # Corrected template path
    context_object_name = 'user_posts'
    login_url = reverse_lazy('login')  # Rediriger si non connecté

    def get_queryset(self):
        # Billets créés par l'utilisateur
        tickets = Ticket.objects.filter(user=self.request.user).annotate(content_type=Value('TICKET', CharField()))

        # Critiques de l'utilisateur en réponse à ses propres billets
        reviews = Review.objects.filter(ticket__user=self.request.user).annotate(
            content_type=Value('REVIEW', CharField()))

        # Combiner et trier les billets et les critiques par ordre antéchronologique
        user_posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        return user_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = self.get_queryset()
        return context
