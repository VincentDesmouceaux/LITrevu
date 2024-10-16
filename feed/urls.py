from django.urls import path
from .views import FeedView, PostView

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/', PostView.as_view(), name='posts'),  # Voir les posts de l'utilisateur
]
