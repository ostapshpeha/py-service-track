from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Operating our notes through admin panel
    """

    list_display = ("order", "author", "date")
    search_fields = ("order__vehicle__number_registration",)
    ordering = ("-date",)
