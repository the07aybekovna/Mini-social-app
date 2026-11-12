from django.db import models

from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    caption = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f'Post by {self.author.username}'

class Reaction(models.Model):

    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reactions'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reactions'
    )

    reaction_type = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_reaction'
            )
        ]

class Comment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username}"