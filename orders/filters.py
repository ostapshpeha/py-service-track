import django_filters
from django import forms

from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    """
    Order filter set to filter by status, client, date from and date to
    """
    status = django_filters.ChoiceFilter(
        choices=Order.Status.choices,
        label="",
        widget=forms.Select(attrs={
            'placeholder': 'Order Status',
            'class': 'form-control form-control-sm'
        })
    )

    client = django_filters.CharFilter(
        field_name="client__last_name",
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Client",
            "class": "form-control form-control-sm"
        })
    )

    date_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="",
        widget=forms.DateInput(attrs={
            "placeholder": "Date from",
            "class": "form-control form-control-sm"
        })
    )

    date_to = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="",
        widget=forms.DateInput(attrs={
            "placeholder": "Date to",
            "class": "form-control form-control-sm"
        })
    )

    class Meta:
        model = Order
        fields = ["status", "client"]
