from django.urls import path

from notes.views import NoteListView, NoteDetailView, NoteCreateView, NoteDeleteView

app_name = "notes"

urlpatterns = [
    path("list/", NoteListView.as_view(), name="note-list"),
    path("<int:pk>/", NoteDetailView.as_view(), name="note-detail"),
    path("create/", NoteCreateView.as_view(), name="note-create"),
    path("<int:pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),
]
