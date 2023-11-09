from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=9,
        widget=forms.NumberInput(attrs={"class": "btn btn-warning", "value": "1"}),
    )


class DiscountApplyForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={"class": "btn btn-warning text-dark"})
    )
