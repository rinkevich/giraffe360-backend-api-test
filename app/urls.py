from django.urls import path
from app import views

urlpatterns = [
    path("events/", views.event_list),
    path("events/<int:pk>/", views.event_detail),
    path("users/<int:user_id>/events/", views.user_list),
    path("repos/<int:repo_id>/events/", views.repo_list),
]