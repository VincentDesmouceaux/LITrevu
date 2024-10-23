from django.urls import path
from .views import FollowsListView, FollowUserView, UnfollowUserView, UserSearchView

urlpatterns = [
    path('follows/', FollowsListView.as_view(), name='follows_list'),
    path('follows/add/', FollowUserView.as_view(), name='follow_user'),
    path('follows/remove/<int:pk>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('follow_search/', UserSearchView.as_view(), name='follow_search'),  # Pour autocomplétion
]
