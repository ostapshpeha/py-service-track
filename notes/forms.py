from django import forms
from django_select2.forms import ModelSelect2Widget

from crm.models import Vehicle
from notes.models import Note


class NoteForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        widget=ModelSelect2Widget(
            model=Vehicle,
            search_fields=[
                "number_registration__icontains",
            ],
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    class Meta:
        model = Note
        fields = ("vehicle", "description", "picture")

class NoteAuthorSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control float-right",
            "placeholder": "Search by author",
        })
    )
