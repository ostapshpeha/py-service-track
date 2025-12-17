from django import forms

from orders.models import Invoice, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class InvoiceForm(forms.ModelForm):
    order = forms.ModelChoiceField(
        label="Cars",
        queryset=Order.objects.none(),
        widget=forms.Select,
        required=True,
    )

    class Meta:
        model = Invoice
        fields = "__all__"