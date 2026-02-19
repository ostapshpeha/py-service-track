import string

from django import forms
from django.core.exceptions import ValidationError
# Removed django_select2 imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div

from crm.models import Vehicle, Client


class VehicleForm(forms.ModelForm):
    """
    Vehicle creating form with vin code validation
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        # Use standard Select widget with tom-select class
        widget=forms.Select(
            attrs={
                "class": "tom-select",
                "placeholder": "Search by client's name",
            }
        ),
        required=False,
        label="Owner",
    )

    class Meta:
        model = Vehicle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('number_registration', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('vin_code', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('engine_type', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Row(
                Column('client', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('last_service', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            Submit('submit', 'Save Vehicle', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-150')
        )

    def clean_vin_code(self):
        vin_code = self.cleaned_data.get("vin_code")
        return validate_vin_code(vin_code)


class VehicleUpdateForm(forms.ModelForm):
    """
    Vehicle update form
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "tom-select",
                "placeholder": "Search by client's name",
            }
        ),
        required=True,
        label="Owner",
    )

    class Meta:
        model = Vehicle
        fields = ("number_registration", "last_service", "client")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('number_registration', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('client', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            'last_service',
            Submit('submit', 'Update Vehicle', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )


class ClientForm(forms.ModelForm):
    """
    Client creating form
    """
    vehicles = forms.ModelMultipleChoiceField(
        queryset=Vehicle.objects.filter(client__isnull=True),
        # Use SelectMultiple with tom-select class
        widget=forms.SelectMultiple(
            attrs={
                "class": "tom-select",
                "placeholder": "Input name, vin or license plate number",
            }
        ),
        required=False,
        label="Vehicle",
    )

    class Meta:
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='w-full md:w-1/2 px-2 mb-4'),
                Column('last_name', css_class='w-full md:w-1/2 px-2 mb-4'),
                css_class='flex flex-wrap -mx-2'
            ),
            'mobile_number',
            'vehicles',
            Submit('submit', 'Save Client', css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 transition duration-150')
        )


class VehicleNumberSearchForm(forms.Form):
    """
    Searching vehicle only by plate number
    """
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control float-right",
            "placeholder": "Search by license plate number",
        })
    )


class ClientLastNameSearchForm(forms.Form):
    """
    Searching client only by last name
    """
    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control float-right",
            "placeholder": "Search by last name",
        })
    )


def validate_vin_code(value: str):
    """
    Custom validator for vin code without Regex
    """
    vin = (value or "").strip()
    if len(vin) != 17:
        raise ValidationError("VIN must be exactly 17 characters long")

    allowed_chars = string.ascii_uppercase + string.digits

    if not all(char in allowed_chars for char in vin):
        raise ValidationError(
            "VIN should have big letters A-Z and numbers (0-9), without spaces"
        )

    return vin
