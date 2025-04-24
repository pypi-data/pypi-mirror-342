"""imaging study URL Configuration."""

from django.urls import path

from dfhir.imagingstudy import views

app_name = "imagingstudy"

urlpatterns = [
    path("imagingstudy/", views.ImagingStudyListView.as_view(), name="list"),
    path(
        "imagingstudy/<int:pk>/", views.ImagingStudyDetailView.as_view(), name="detail"
    ),
]
