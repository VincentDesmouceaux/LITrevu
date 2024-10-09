from django import forms
from .models import Ticket, Review

# Formulaire pour la création et la modification des billets (Tickets)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']  # Les champs que tu veux exposer dans le formulaire
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

# Formulaire pour la création/modification des critiques


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la critique'}),
            'rating': forms.RadioSelect(),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Commentaire'}),
        }
