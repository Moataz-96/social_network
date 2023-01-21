# users/urls.py

from django.urls import path
from users import views

urlpatterns = [
    path('filter/', views.filter, name='users_filter'),
    path('all/', views.retrieve_all_users, name='retrieve_all_users'),
    path('active/', views.retrieve_active_users, name='retrieve_active_users'),

    path("details/<str:pk>/", views.details, name="user_details"),
    path("update/<str:pk>/", views.update, name="user_update"),
    path("delete/soft/<str:pk>/", views.soft_delete, name="user_soft_delete"),
    path("delete/hard/<str:pk>/", views.hard_delete, name="user_hard_delete"),

    path('login/', views.login, name='user_login'),
    path('signup/', views.signup, name='users_signup'),
    path('activate/<str:pk>/', views.activate, name='users_activate'),
    path('change_password/<str:pk>/', views.change_password, name='change_password'),
]
