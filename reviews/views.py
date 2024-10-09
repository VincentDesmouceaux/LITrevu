from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm

# Critique en réponse à un ticket existant


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form_response.html'  # Template pour les critiques liées à un ticket
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_range'] = range(6)
        context['ticket'] = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        return context

    def form_valid(self, form):
        # Associer le ticket à la critique avant de la sauvegarder
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        form.instance.ticket = ticket
        form.instance.user = self.request.user
        return super().form_valid(form)


# Critique indépendante (sans ticket)
class ReviewCreateWithoutTicketView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'  # Assure-toi que c'est bien le nom de ton template
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_range'] = range(6)  # Définit la plage de 0 à 5 pour les notes
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_edit.html'  # Assurez-vous que c'est bien ce fichier
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object()
        context['ticket'] = self.get_object().ticket  # Récupère le ticket lié à la critique
        context['rating_range'] = range(6)  # Pour afficher les notes de 0 à 5
        return context

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


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


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
