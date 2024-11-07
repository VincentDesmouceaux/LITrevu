from django import forms
from .models import Ticket, Review

# Formulaire pour la création et la modification des billets (Tickets)


class TicketForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'un billet (Ticket).

    Champs :
        title : Champ texte pour le titre du billet.
        description : Champ texte pour la description du billet, avec une zone de texte de 4 lignes.
        image : Champ de fichier pour uploader une image associée au billet.
    """

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

# Formulaire pour la création/modification des critiques


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'une critique (Review).

    Champs :
        headline : Champ texte pour le titre de la critique.
        rating : Champ de sélection pour la note de la critique, de 1 à 5 étoiles.
        body : Champ texte pour le corps de la critique, avec une zone de texte de 5 lignes.
    """

    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
