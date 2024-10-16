from django.urls import path
from .views import UserLoginView, UserLogoutView, UserSignUpView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
]