from django import forms
# Removed django_select2 imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div

from crm.models import Vehicle
from notes.models import Note


class NoteForm(forms.ModelForm):
    """
    Note form with searching car
    """
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all().order_by("name"),
        # Use standard Select widget with tom-select class
        widget=forms.Select(
            attrs={
                "class": "tom-select",
                "placeholder": "Input license plate number",
            }
        ),
        required=True,
    )

    class Meta:
        model = Note
        fields = ("vehicle", "description", "picture")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'vehicle',
            'description',
            'picture',
            Submit('submit', 'Save Note', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )


class NoteAuthorSearchForm(forms.Form):
    """
    Searching notes only by author's first abd last name
    """
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control float-right",
            "placeholder": "Search by author",
        })
    )
