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

        for ticket in tickets:
            ticket.has_user_reviewed = reviews.filter(ticket=ticket, user=self.request.user).exists()

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
    template_name = 'feed/posts.html'
    context_object_name = 'user_posts'
    login_url = reverse_lazy('login')  # Rediriger si non connecté

    def get_queryset(self):
        tickets = Ticket.objects.filter(user=self.request.user).annotate(content_type=Value('TICKET', CharField()))
        reviews = Review.objects.filter(ticket__user=self.request.user).annotate(
            content_type=Value('REVIEW', CharField()))

        user_posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )

        return user_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = self.get_queryset()
        context['rating_range'] = [1, 2, 3, 4, 5]  # Ajout pour simuler range(1, 6)
        return context
