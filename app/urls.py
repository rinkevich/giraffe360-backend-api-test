from django.urls import path
from app import views

urlpatterns = [
    path("events/", views.EventCreateView.as_view()),
    path("events/<int:pk>/", views.EventListView.as_view()),
    path("users/<int:user_id>/events/", views.UserListView.as_view()),
    path("repos/<int:repo_id>/events/", views.RepoListView.as_view()),
]