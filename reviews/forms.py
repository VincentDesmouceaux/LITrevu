from django import forms
from .models import Ticket, Review

# Formulaire pour la création et la modification des billets (Tickets)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# Formulaire pour la création/modification des critiques


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
