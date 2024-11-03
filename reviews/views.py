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
    template_name = 'reviews/review_form_response.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        print(f"[DEBUG] Récupération du ticket_id pour ReviewCreateView : {ticket_id}")
        context['ticket'] = get_object_or_404(Ticket, id=ticket_id)
        return context

    def form_valid(self, form):
        ticket_id = self.kwargs.get('ticket_id')
        print(f"[DEBUG] Association du ticket_id {ticket_id} à la critique dans ReviewCreateView")
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form.instance.ticket = ticket
        form.instance.user = self.request.user
        return super().form_valid(form)

# Critique sans ticket associé


class ReviewCreateWithoutTicketView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("[DEBUG] Accès à ReviewCreateWithoutTicketView")
        context['rating_range'] = range(1, 6)
        return context

    def form_valid(self, form):
        title = self.request.POST.get('title')
        description = self.request.POST.get('description')
        image = self.request.FILES.get('file')

        # Log des données récupérées
        print(f"[DEBUG] Titre: {title}, Description: {description}, Image: {image}")

        if not title or not description:
            form.add_error(None, "Le titre et la description du billet sont requis.")
            print("[DEBUG] Erreur : Le titre ou la description est manquant dans ReviewCreateWithoutTicketView")
            return self.form_invalid(form)

        ticket = Ticket.objects.create(
            title=title,
            description=description,
            user=self.request.user,
            image=image
        )
        print(f"[DEBUG] Ticket créé avec succès : {ticket}")

        form.instance.ticket = ticket
        form.instance.user = self.request.user
        return super().form_valid(form)

# Modification d'une critique existante


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_edit.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        print(f"[DEBUG] Modification de la critique avec ID : {review.id}")
        context['review'] = review
        context['ticket'] = review.ticket
        return context

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

# Création d'un nouveau billet


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket_create.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        print(f"[DEBUG] Création d'un ticket par l'utilisateur {self.request.user}")
        form.instance.user = self.request.user
        return super().form_valid(form)

# Modification d'un billet existant


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket_edit.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        print(f"[DEBUG] Filtrage des tickets pour l'utilisateur {self.request.user}")
        return Ticket.objects.filter(user=self.request.user)

# Suppression d'un billet


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'reviews/ticket_confirm_delete.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        print(f"[DEBUG] Filtrage des tickets pour suppression par l'utilisateur {self.request.user}")
        return Ticket.objects.filter(user=self.request.user)

# Suppression d'une critique


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('homepage')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        print(f"[DEBUG] Filtrage des critiques pour suppression par l'utilisateur {self.request.user}")
        return Review.objects.filter(user=self.request.user)
