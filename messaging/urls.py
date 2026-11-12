from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:conversation_id>/', views.chat, name='chat'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
]