from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.db import transaction

from .models import Conversation


User = get_user_model()


@login_required(login_url='/accounts/login/')
def inbox(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related(
        'participants',
        'messages'
    ).order_by('-updated_at')

    search_query = request.GET.get('q', '').strip()

    users = User.objects.none()

    if search_query:
        users = User.objects.filter(
            username__icontains=search_query
        ).exclude(
            id=request.user.id
        )[:10]

    return render(request, 'messages/inbox.html', {
        'conversations': conversations,
        'users': users,
        'search_query': search_query
    })

@login_required(login_url='/accounts/login/')
def chat(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.filter(participants=request.user),
        id=conversation_id
    )

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            conversation.messages.create(
                sender=request.user,
                content=content
            )

            conversation.save(update_fields=['updated_at'])

        return redirect('chat', conversation_id=conversation.id)

    conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(is_read=True)

    messages = conversation.messages.select_related(
        'sender'
    ).all()

    other_participants = conversation.participants.exclude(
        id=request.user.id
    )

    return render(request, 'messages/chat.html', {
        'conversation': conversation,
        'messages': messages,
        'other_participants': other_participants
    })


@login_required(login_url='/accounts/login/')
@require_POST
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('inbox')

    with transaction.atomic():
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).annotate(
            participant_count=Count('participants', distinct=True)
        ).filter(
            participant_count=2
        ).first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(
                request.user,
                other_user
            )

    return redirect('chat', conversation_id=conversation.id)