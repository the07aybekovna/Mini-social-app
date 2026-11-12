from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),

    path(
        '<int:post_id>/reaction/',
        views.reaction_view,
        name='reaction'
    ),

    path(
        '<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        '<int:comment_id>/delete-comment/',
        views.delete_comment,
        name='delete_comment'
    ),
    path(
    '<int:post_id>/delete/',
    views.delete_post,
    name='delete_post'
),
]