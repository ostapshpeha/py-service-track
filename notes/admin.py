from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Operating our notes through admin panel
    """
    list_display = ("vehicle", "author", "date")
    search_fields = ("vehicle__number_registration",)
    ordering = ("-date",)
