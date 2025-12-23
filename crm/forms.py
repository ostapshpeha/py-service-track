import re

from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from crm.models import Vehicle, Client


class VehicleForm(forms.ModelForm):
    """
    Vehicle creating form with vin code validation
    and easier searching+select system Select2 to
    choose the owner of the vehicle
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=Client,
            search_fields=[
                "last_name__icontains",
                "first_name__icontains",
            ],
            attrs={
                "class": "form-control",
                "data-placeholder": "Search by client's name",
            }
        ),
        required=False,
        label="Owner",
    )

    class Meta:
        model = Vehicle
        fields = "__all__"

    def clean_vin_code(self):
        vin_code = self.cleaned_data.get("vin_code")
        return validate_vin_code(vin_code)


class VehicleUpdateForm(forms.ModelForm):
    """
    Vehicle update form with Select2 widget
    Fields to update: client(owner), number, last service
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=Client,
            search_fields=[
                "last_name__icontains",
                "first_name__icontains",
            ],
            attrs={
                "class": "form-control",
                "data-placeholder": "Search by client's name",
            }
        ),
        required=True,
        label="Owner",
    )

    class Meta:
        model = Vehicle
        fields = ("number_registration", "last_service", "client")


class ClientForm(forms.ModelForm):
    """
    Client creating form with widget Select2 to search
    vehicle by number, vin code and name
    """
    vehicles = forms.ModelMultipleChoiceField(
        queryset=Vehicle.objects.filter(client__isnull=True),
        widget=ModelSelect2MultipleWidget(
            model=Vehicle,
            search_fields=[
                "number_registration__icontains",
                "vin_code__icontains",
                "name__icontains",
            ],
            attrs={
                "class": "form-control",
                "data-placeholder": "Input name, vin or license plate number",
            }
        ),
        required=False,
        label="Vehicle",
    )

    class Meta:
        model = Client
        fields = "__all__"


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


_VIN_RE = re.compile(r"^[A-Z0-9]{17}$")


def validate_vin_code(value: str):
    """
    Custom validator for vin code
    """
    vin = (value or "").strip()

    if len(vin) != 17:
        raise ValidationError("VIN must be exactly 17 characters long")

    if not _VIN_RE.fullmatch(vin):
        raise ValidationError(
            "VIN should have big letters A-Z and numbers (0-9), without spaces"
        )

    return vin
