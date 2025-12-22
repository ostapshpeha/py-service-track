from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import generic

from notes.forms import NoteForm, NoteAuthorSearchForm
from notes.models import Note


class NoteListView(LoginRequiredMixin, generic.ListView):
    """
    Note list view with searching through author's first and last name
    """
    model = Note
    paginate_by = 30
    context_object_name = "notes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NoteAuthorSearchForm(
            self.request.GET or None
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = NoteAuthorSearchForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data["q"]
            if q:
                queryset = queryset.filter(
                  Q(author__last_name__icontains=q) |
                  Q(author__first_name__icontains=q)
                )

        return queryset


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Note detail view
    """
    model = Note


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Note create view with form validation
    Redirect to note detail view
    """
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("notes:note-list")

    def get_success_url(self):
        return reverse(
            "notes:note-detail",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        """
        Auto choosing the author of the note
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Note delete view
    """
    model = Note
    success_url = reverse_lazy("notes:note-list")
