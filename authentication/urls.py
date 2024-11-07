from django.urls import path
from .views import UserLoginView, UserLogoutView, UserSignUpView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # Vue pour la connexion
    path('logout/', UserLogoutView.as_view(), name='logout'),  # Vue pour la déconnexion
    path('signup/', UserSignUpView.as_view(), name='signup'),  # Vue pour l'inscription
]
