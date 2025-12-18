from django import forms

from orders.models import Invoice, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].label = "Cars"
        self.fields["order"].queryset = Order.objects.filter(invoice__isnull=True)