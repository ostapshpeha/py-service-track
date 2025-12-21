from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import generic

from notes.forms import NoteForm, NoteAuthorSearchForm
from notes.models import Note


class NoteListView(LoginRequiredMixin, generic.ListView):
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
                  Q(author__last_name__icontains=q) | Q(author__first_name__icontains=q)
                )

        return queryset


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("notes:note-list")

    def get_success_url(self):
        return reverse(
            "notes:note-detail",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Note
    success_url = reverse_lazy("notes:note-list")
