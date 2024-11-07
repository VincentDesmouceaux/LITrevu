from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authentication.views import HomePageView, UserLogoutView, UserSignUpView, UserLoginView
from reviews.views import (
    TicketCreateView, TicketUpdateView, TicketDeleteView,
    ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    ReviewCreateWithoutTicketView
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin site
    path('', HomePageView.as_view(), name='homepage'),  # Home page view
    path('auth/login/', UserLoginView.as_view(), name='login'),  # Login URL
    path('auth/logout/', UserLogoutView.as_view(), name='logout'),  # Logout URL
    path('auth/signup/', UserSignUpView.as_view(), name='signup'),  # Signup URL
    path('ticket/add/', TicketCreateView.as_view(), name='ticket-add'),  # Create new ticket
    path('ticket/<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket-edit'),  # Edit existing ticket
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),  # Delete ticket
    path('ticket/<int:ticket_id>/review/add/', ReviewCreateView.as_view(), name='review-add'),  # Add review to a ticket
    path('review/create/', ReviewCreateWithoutTicketView.as_view(),
         name='review-create'),  # Create review without a ticket
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),  # Edit review
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),  # Delete review
    path('subscriptions/', include('subscriptions.urls')),  # Subscription functionality
    path('feed/', include('feed.urls')),  # Feed functionality
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
