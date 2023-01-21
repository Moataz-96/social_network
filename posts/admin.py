# users/admin.py

from django.contrib import admin
from posts.models import Post, PostLike

admin.site.register(Post)
admin.site.register(PostLike)