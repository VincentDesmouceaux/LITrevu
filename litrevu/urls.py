from django.contrib import admin
from django.urls import path, include
from authentication.views import HomePageView
from reviews.views import (
    TicketCreateView, TicketUpdateView, TicketDeleteView,
    ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    ReviewCreateWithoutTicketView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),
    path('auth/', include('authentication.urls')),
    path('ticket/add/', TicketCreateView.as_view(), name='ticket-add'),
    path('ticket/<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket-edit'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('ticket/<int:ticket_id>/review/add/', ReviewCreateView.as_view(),
         name='review-add'),  # Critique en réponse à un ticket
    path('review/create/', ReviewCreateWithoutTicketView.as_view(), name='review-create'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
