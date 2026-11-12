from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=300, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='following'
    )

    following = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='followers'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            )
        ]

def __str__(self):
    return f"{self.follower} follows {self.following}"

class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('comment', 'Comment'),
    ]

    # Notification kimga yuboriladi?
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # Notificationni kim yaratdi?
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    # Qaysi post bilan bog‘liq? (Follow uchun shart emas)
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender} - {self.notification_type} - {self.recipient}'