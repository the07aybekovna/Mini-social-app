from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from .forms import RegisterForm, EditProfileForm
from .models import Follow, User, Notification
from posts.models import Post, Reaction
from django.utils.dateparse import parse_date



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def home(request):
    posts = Post.objects.select_related('author').annotate(
        likes_count=Count(
            'reactions',
            filter=Q(reactions__reaction_type='like'),
            distinct=True
        ),
        dislikes_count=Count(
            'reactions',
            filter=Q(reactions__reaction_type='dislike'),
            distinct=True
        )
    ).prefetch_related(
        Prefetch(
            'reactions',
            queryset=Reaction.objects.filter(user=request.user),
            to_attr='user_reactions'
        )
    )

    return render(request, 'accounts/home.html', {
        'posts': posts
    })


@login_required(login_url='login')
def profile_view(request):
    posts = request.user.posts.all()

    return render(request, 'accounts/profile.html', {
        'profile_user': request.user,
        'posts': posts,
        'followers_count': request.user.followers.count(),
        'following_count': request.user.following.count()
    })


@login_required(login_url='login')
def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile_user.followers.count(),
        'following_count': profile_user.following.count()
    })


@login_required(login_url='login')
def follow_toggle_view(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('profile')

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )

    if follow.exists():
        # Unfollow
        follow.delete()

    else:
        # Follow
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

        # Notification yaratamiz
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow'
        )

    return redirect('user_profile', username=username)


@login_required
def followers_list_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    follows = Follow.objects.filter(
        following=profile_user
    ).select_related('follower')

    return render(request, 'accounts/follow_list.html', {
        'profile_user': profile_user,
        'follows': follows,
        'list_type': 'Followers'
    })


@login_required
def following_list_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    follows = Follow.objects.filter(
        follower=profile_user
    ).select_related('following')

    return render(request, 'accounts/follow_list.html', {
        'profile_user': profile_user,
        'follows': follows,
        'list_type': 'Following'
    })


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })


@login_required(login_url='login')
def explore_view(request):
    users = User.objects.exclude(
        id=request.user.id
    ).annotate(
        followers_count=Count('followers', distinct=True)
    )


    search_query = request.GET.get('q', '').strip()

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )


    min_followers = request.GET.get('min_followers', '').strip()
    max_followers = request.GET.get('max_followers', '').strip()

    if min_followers.isdigit():
        users = users.filter(
            followers_count__gte=int(min_followers)
        )

    if max_followers.isdigit():
        users = users.filter(
            followers_count__lte=int(max_followers)
        )


    joined_after = request.GET.get('joined_after', '').strip()
    joined_before = request.GET.get('joined_before', '').strip()

    after_date = parse_date(joined_after) if joined_after else None
    before_date = parse_date(joined_before) if joined_before else None

    if after_date:
        users = users.filter(
            date_joined__date__gte=after_date
        )

    if before_date:
        users = users.filter(
            date_joined__date__lte=before_date
        )


    has_bio = request.GET.get('has_bio', '')
    has_avatar = request.GET.get('has_avatar', '')

    if has_bio == 'yes':
        users = users.exclude(bio='')

    if has_avatar == 'yes':
        users = users.exclude(avatar='')


    sort_by = request.GET.get('sort', 'newest')

    if sort_by == 'oldest':
        users = users.order_by('date_joined')

    elif sort_by == 'followers':
        users = users.order_by('-followers_count')

    elif sort_by == 'username':
        users = users.order_by('username')

    else:
        sort_by = 'newest'
        users = users.order_by('-date_joined')


    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)


    context = {
        'users': users,
        'search_query': search_query,

        'min_followers': min_followers,
        'max_followers': max_followers,

        'joined_after': joined_after,
        'joined_before': joined_before,

        'has_bio': has_bio,
        'has_avatar': has_avatar,

        'sort_by': sort_by,

        'following_ids': following_ids,
    }

    return render(
        request,
        'accounts/explore.html',
        context
    )


@login_required(login_url='login')
def notifications_view(request):
    notifications = request.user.notifications.select_related(
        'sender', 'post'
    ).all()

    unread_count = notifications.filter(is_read=False).count()

    return render(request, 'accounts/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
