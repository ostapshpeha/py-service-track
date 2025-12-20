import re

from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from crm.models import Vehicle, Client


class VehicleForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2Widget(
            model=Client,
            search_fields=[
                "last_name__icontains",
                "first_name__icontains",
            ],
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    class Meta:
        model = Vehicle
        fields = "__all__"

    def clean_vin_code(self):
        vin_code = self.cleaned_data.get("vin_code")
        return validate_vin_code(vin_code)

class VehicleUpdateForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2Widget(
            model=Client,
            search_fields=[
                "last_name__icontains",
                "first_name__icontains",
            ],
            attrs={"class": "form-control"}
        ),
        required=True,
    )
    class Meta:
        model = Vehicle
        fields = ("number_registration", "last_service", "client")


class ClientForm(forms.ModelForm):
    vehicles = forms.ModelMultipleChoiceField(
        queryset=Vehicle.objects.filter(client__isnull=True),
        widget=ModelSelect2MultipleWidget(
            model=Vehicle,
            search_fields=[
                "number_registration__icontains",
                "vin_code__icontains",
                "name__icontains",
            ],
        ),
        required=False,
    )

    class Meta:
        model = Client
        fields = "__all__"


_VIN_RE = re.compile(r"^[A-Z0-9]{17}$")

def validate_vin_code(value: str):
    vin = (value or "").strip()

    if len(vin) != 17:
        raise ValidationError("VIN must be exactly 17 characters long")

    if not _VIN_RE.fullmatch(vin):
        raise ValidationError("VIN should have big letters A-Z and numbers (0-9), without spaces")

    return vin
