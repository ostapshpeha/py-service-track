from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from notes.forms import NoteForm
from notes.models import Note


class NoteListView(LoginRequiredMixin, generic.ListView):
    model = Note
    paginate_by = 30
    context_object_name = "notes"


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("notes:note-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Note
    success_url = reverse_lazy("notes:note-list")
