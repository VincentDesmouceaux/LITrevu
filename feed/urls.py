from django.urls import path
from .views import FeedView, PostView

# URL configuration pour le flux et les posts de l'utilisateur
urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),  # Flux d'activités
    path('posts/', PostView.as_view(), name='posts'),  # Posts de l'utilisateur
]
