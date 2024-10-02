from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm


class HomePageView(TemplateView):
    template_name = 'reviews/homepage.html'  # Chemin correct pour le template de la page d'accueil

    def get(self, request, *args, **kwargs):
        print(f"Utilisateur sur la page d'accueil : {request.user}")
        print(f"Authentifié ? {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket_create.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket_edit.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'reviews/ticket_confirm_delete.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_edit.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
