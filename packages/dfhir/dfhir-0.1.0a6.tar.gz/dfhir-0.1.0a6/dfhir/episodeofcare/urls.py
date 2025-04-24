"""Episode of care urls."""

from django.urls import path

from . import views

app_name = "episodeofcare"

urlpatterns = [
    path("episodeofcare/", views.EpisodeOfCareListView.as_view()),
    path("episodeofcare/<int:pk>/", views.EpisodeOfCareDetailView.as_view()),
]
