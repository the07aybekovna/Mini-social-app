from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm
from .models import Post, Reaction, Comment
from accounts.models import Notification
from django.http import JsonResponse


@login_required(login_url='/accounts/login/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
@require_POST
def reaction_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    reaction_type = request.POST.get('reaction_type')

    if reaction_type not in ['like', 'dislike']:
        return JsonResponse({
            'success': False,
            'error': 'Invalid reaction type'
        }, status=400)

    reaction = Reaction.objects.filter(
        user=request.user,
        post=post
    ).first()

    if reaction:
        if reaction.reaction_type == reaction_type:
            reaction.delete()
        else:
            reaction.reaction_type = reaction_type
            reaction.save()
    else:
        Reaction.objects.create(
            user=request.user,
            post=post,
            reaction_type=reaction_type
        )

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            sender=request.user,
            post=post,
            notification_type=reaction_type
        )

    return redirect('home')


@login_required(login_url='/accounts/login/')
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                post=post,
                notification_type='comment'
            )

    return redirect('home')


@login_required(login_url='/accounts/login/')
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    comment.delete()

    return redirect('home')


@login_required(login_url='/accounts/login/')
@require_POST
def delete_post(request, post_id):
    # Faqat joriy foydalanuvchining postini topamiz
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    # Postni o‘chiramiz
    post.delete()

    return redirect('home')
