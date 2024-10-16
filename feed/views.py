from django.views.generic import ListView
from django.db.models import Q, Value, CharField
from itertools import chain
from reviews.models import Ticket, Review


class FeedView(ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Billets créés par l'utilisateur ou par les utilisateurs qu'il suit
        tickets = Ticket.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all())
        ).annotate(content_type=Value('TICKET', CharField()))

        # Critiques créées par l'utilisateur, les utilisateurs qu'il suit, ou en réponse à ses billets
        reviews = Review.objects.filter(
            Q(user=self.request.user) |
            Q(user__in=self.request.user.follows.all()) |
            Q(ticket__user=self.request.user)
        ).annotate(content_type=Value('REVIEW', CharField()))

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
