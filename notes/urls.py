from django.urls import path

from notes.views import NoteListView, NoteDetailView, NoteCreateView, NoteDeleteView

app_name = "notes"

urlpatterns = [
    path("notes/", NoteListView.as_view(), name="note-list"),
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note-detail"),
    path("notes/create/", NoteCreateView.as_view(), name="note-create"),
    path("notes/<int:pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),
    ]