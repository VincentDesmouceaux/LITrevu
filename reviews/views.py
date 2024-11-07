from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm

# Critique en réponse à un ticket existant


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer une critique en réponse à un ticket existant.
    Utilise `ReviewForm` pour le formulaire et redirige vers la page de flux après la création.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form_response.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """
        Ajoute le contexte du ticket associé pour que le formulaire de critique 
        puisse afficher les détails du ticket.
        """
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        print(f"[DEBUG] Récupération du ticket_id pour ReviewCreateView : {ticket_id}")
        context['ticket'] = get_object_or_404(Ticket, id=ticket_id)
        return context

    def form_valid(self, form):
        """
        Associe la critique au ticket et à l'utilisateur avant de l'enregistrer.
        """
        ticket_id = self.kwargs.get('ticket_id')
        print(f"[DEBUG] Association du ticket_id {ticket_id} à la critique dans ReviewCreateView")
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form.instance.ticket = ticket
        form.instance.user = self.request.user
        return super().form_valid(form)

# Critique sans ticket associé


class ReviewCreateWithoutTicketView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer une critique sans ticket associé. Un ticket est créé avec 
    la critique pour permettre le suivi.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """
        Ajoute une plage de notation pour la critique dans le contexte.
        """
        context = super().get_context_data(**kwargs)
        print("[DEBUG] Accès à ReviewCreateWithoutTicketView")
        context['rating_range'] = range(1, 6)
        return context

    def form_valid(self, form):
        """
        Crée un ticket avec la critique pour assurer une structure uniforme.
        Vérifie que le titre et la description sont fournis avant de créer le ticket.
        """
        title = self.request.POST.get('title')
        description = self.request.POST.get('description')
        image = self.request.FILES.get('file')

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
    """
    Vue pour modifier une critique existante. Permet de modifier les critiques
    créées par l'utilisateur ou celles liées aux tickets de l'utilisateur.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_edit.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """
        Ajoute le contexte pour afficher le ticket associé à la critique dans le formulaire de modification.
        """
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        print(f"[DEBUG] Modification de la critique avec ID : {review.id}")
        context['review'] = review
        context['ticket'] = review.ticket
        return context

    def get_queryset(self):
        """
        Permet uniquement la modification des critiques appartenant à l'utilisateur ou
        celles associées à des tickets de l'utilisateur.
        """
        print(f"[DEBUG] Filtrage des critiques pour modification par l'utilisateur {self.request.user}")
        return Review.objects.filter(Q(user=self.request.user) | Q(ticket__user=self.request.user))

# Suppression d'une critique


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue pour supprimer une critique existante. Permet de supprimer les critiques
    créées par l'utilisateur ou celles liées aux tickets de l'utilisateur.
    """
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        """
        Permet uniquement la suppression des critiques appartenant à l'utilisateur ou
        celles associées à des tickets de l'utilisateur.
        """
        print(f"[DEBUG] Filtrage des critiques pour suppression par l'utilisateur {self.request.user}")
        return Review.objects.filter(Q(user=self.request.user) | Q(ticket__user=self.request.user))

# Création d'un nouveau billet


class TicketCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer un nouveau billet. Associe le billet à l'utilisateur 
    connecté avant de l'enregistrer.
    """
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket_create.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Associe le billet à l'utilisateur avant de l'enregistrer.
        """
        print(f"[DEBUG] Création d'un ticket par l'utilisateur {self.request.user}")
        form.instance.user = self.request.user
        return super().form_valid(form)

# Modification d'un billet existant


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue pour modifier un billet existant. Limite les billets modifiables 
    à ceux de l'utilisateur connecté.
    """
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket_edit.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        """
        Limite le queryset aux billets de l'utilisateur connecté.
        """
        print(f"[DEBUG] Filtrage des tickets pour l'utilisateur {self.request.user}")
        return Ticket.objects.filter(user=self.request.user)

# Suppression d'un billet


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue pour supprimer un billet existant. Limite les billets supprimables 
    à ceux de l'utilisateur connecté.
    """
    model = Ticket
    template_name = 'reviews/ticket_confirm_delete.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        """
        Limite le queryset aux billets de l'utilisateur connecté.
        """
        print(f"[DEBUG] Filtrage des billets pour suppression par l'utilisateur {self.request.user}")
        return Ticket.objects.filter(user=self.request.user)
