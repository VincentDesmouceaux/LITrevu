from django.contrib import admin
from django.urls import path, include
from reviews.views import HomePageView, TicketCreateView, TicketUpdateView, TicketDeleteView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),  # Page d'accueil
    path('auth/', include('authentication.urls')),  # URLs d'authentification
    # URLs pour les billets (Tickets)
    path('ticket/add/', TicketCreateView.as_view(), name='ticket-add'),
    path('ticket/<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket-edit'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    # URLs pour les critiques (Reviews)
    path('ticket/<int:ticket_id>/review/add/', ReviewCreateView.as_view(), name='review-add'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
