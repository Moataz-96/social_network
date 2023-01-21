# posts/models.py
from users.models import CustomUser
from django.db import models
from posts.manager import ActiveManager
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'post'
        ordering = ('created_at',)
        indexes = [
            models.Index(fields=['id'], name='post_id'),
            models.Index(fields=['user'], name='post_user'),
            models.Index(fields=['description'], name='post_description'),
        ]


class PostLike(models.Model):
    DEFAULT = 0
    LIKE = 1
    UNLIKE = 2
    like_stats_choices = (
        (DEFAULT, 'default'),
        (LIKE, 'like'),
        (UNLIKE, 'unlike')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    status = models.IntegerField(default=DEFAULT, null=False, choices=like_stats_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'post_like'
        ordering = ('created_at',)
        unique_together = ('user', 'post',)
        indexes = [
            models.Index(fields=['id'], name='postlike_id'),
            models.Index(fields=['status'], name='postlike_status'),
            models.Index(fields=['id', 'status'], name='postlike_id_status')
        ]
