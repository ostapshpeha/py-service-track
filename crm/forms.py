import re

from django import forms
from django.core.exceptions import ValidationError

from crm.models import Vehicle, Client


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

    def clean_vin_code(self):
        vin_code = self.cleaned_data.get("vin_code")
        return validate_vin_code(vin_code)


class ClientForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        label="Cars",
        queryset=Vehicle.objects.none(),
        widget=forms.SelectMultiple,
        required=False,
    )
    class Meta:
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        pass


_VIN_RE = re.compile(r"^[A-Z0-9]{17}$")

def validate_vin_code(value: str):
    vin = (value or "").strip()

    if len(vin) != 17:
        raise ValidationError("VIN must be exactly 17 characters long")

    if not _VIN_RE.fullmatch(vin):
        raise ValidationError("VIN should have big letters A-Z and numbers (0-9), without spaces")

    return vin
