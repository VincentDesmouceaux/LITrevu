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


class ReviewCreateWithoutTicketView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_range'] = range(6)
        return context

    def form_valid(self, form):
        title = self.request.POST.get('title')
        description = self.request.POST.get('description')
        image = self.request.FILES.get('file')

        # Log les données récupérées
        print(f"Title: {title}, Description: {description}, Image: {image}")

        # Assurez-vous que 'title' et 'description' sont bien présents
        if not title or not description:
            form.add_error(None, "Le titre et la description du billet sont requis.")
            print("Erreur : Le titre ou la description est manquant.")
            return self.form_invalid(form)

        # Créez le billet associé à la critique
        ticket = Ticket.objects.create(
            title=title,
            description=description,
            user=self.request.user,
            image=image
        )
        print(f"Ticket créé : {ticket}")

        # Associez le ticket à la critique avant de la sauvegarder
        form.instance.ticket = ticket
        form.instance.user = self.request.user

        # Appel à la méthode super pour sauvegarder la critique
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
