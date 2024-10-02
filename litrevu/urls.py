from django.contrib import admin
from django.urls import path
from reviews.views import UserLoginView, UserLogoutView, UserSignUpView, HomePageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),  # Page d'accueil
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
]
