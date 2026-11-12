from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    path(
        'users/<str:username>/',
        views.user_profile_view,
        name='user_profile'
    ),

    path(
        'users/<str:username>/follow/',
        views.follow_toggle_view,
        name='follow_toggle'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'users/<str:username>/followers/',
         views.followers_list_view,
         name='followers_list'
    ),
    path(
         'users/<str:username>/following/',
         views.following_list_view,
         name='following_list'
    ),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('explore/', views.explore_view, name='explore'),
    path('notifications/', views.notifications_view, name='notifications'),
]