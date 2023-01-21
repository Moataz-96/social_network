# users/urls.py

from django.urls import path
from posts import views

urlpatterns = [
    # CRUD Operations
    path("create/", views.create, name="post_details"),
    path("retrieve/<str:pk>/", views.retrieve, name="post_details"),
    path("update/<str:pk>/", views.update, name="post_update"),
    path("delete/soft/<str:pk>/", views.soft_delete, name="post_soft_delete"),
    path("delete/hard/<str:pk>/", views.hard_delete, name="post_hard_delete"),

    # View posts
    path('all/', views.retrieve_all_posts, name='retrieve_all_users'),
    path('active/', views.retrieve_active_posts, name='retrieve_active_users'),
    path("user/<str:pk>/", views.retrieve_user_posts, name="user_posts"),

    # Filter posts
    path('contains/', views.contains, name='posts_contains'),

    # Post likes
    path('<str:pk>/status/like/', views.status_like, name='post_like'),
    path('<str:pk>/status/unlike/', views.status_unlike, name='post_unlike'),
    path('<str:pk>/status/default/', views.status_default, name='post_default'),
]
