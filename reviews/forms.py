from django import forms
from .models import Ticket, Review

# Formulaire pour la création et la modification des billets (Tickets)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Description'}),
        }

# Formulaire pour la création/modification des critiques


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la critique'}),
            'rating': forms.RadioSelect(),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Commentaire'}),
        }
