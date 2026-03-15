from django import forms

# Removed django_select2 imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from orders.models import Order
from notes.models import Note


class NoteForm(forms.ModelForm):
    """
    Note form with searching order
    """

    order = forms.ModelChoiceField(
        queryset=Order.objects.all().order_by("-created_at"),
        # Use standard Select widget with tom-select class
        widget=forms.Select(
            attrs={
                "class": "tom-select",
                "placeholder": "Select order",
            }
        ),
        required=True,
    )

    class Meta:
        model = Note
        fields = ("order", "description", "picture")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "order",
            "description",
            "picture",
            Submit(
                "submit",
                "Save Note",
                css_class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150",
            ),
        )


class NoteAuthorSearchForm(forms.Form):
    """
    Searching notes only by author's first abd last name
    """

    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control float-right",
                "placeholder": "Search by author",
            }
        ),
    )
