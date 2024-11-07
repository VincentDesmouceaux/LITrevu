from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """
    Modèle représentant un billet (ticket), avec un titre, une description optionnelle,
    une image associée et une relation avec l'utilisateur qui l'a créé.

    Attributs :
        title (CharField) : Titre du billet (max 128 caractères).
        description (TextField) : Description détaillée du billet (optionnelle).
        user (ForeignKey) : Utilisateur ayant créé le billet (lié à AUTH_USER_MODEL).
        image (ImageField) : Image associée au billet, uploadée dans 'ticket_images/'.
        time_created (DateTimeField) : Date et heure de création du billet.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets'
    )
    image = models.ImageField(null=True, blank=True, upload_to='ticket_images/')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retourne le titre du billet comme représentation de l'instance."""
        return self.title

    def get_reviews(self):
        """
        Retourne toutes les critiques (reviews) associées à ce ticket.

        Returns:
            QuerySet : Ensemble des critiques liées au billet.
        """
        return self.reviews.all()


class Review(models.Model):
    """
    Modèle représentant une critique (review) d'un billet, avec un titre, une note,
    un corps de texte, et une relation avec l'utilisateur et le ticket associé.

    Attributs :
        ticket (ForeignKey) : Le billet auquel la critique est associée (optionnel).
        rating (PositiveSmallIntegerField) : Note de la critique, entre 0 et 5.
        headline (CharField) : Titre de la critique (max 128 caractères).
        body (TextField) : Texte détaillé de la critique (optionnel).
        user (ForeignKey) : Utilisateur ayant créé la critique (lié à AUTH_USER_MODEL).
        time_created (DateTimeField) : Date et heure de création de la critique.
    """

    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retourne le titre de la critique comme représentation de l'instance."""
        return self.headline
