from django import forms
from .models import Transfer, Subdivision


class TransferForm(forms.ModelForm):
    # email = forms.EmailField(max_length=100, help_text='Buyer email.')

    class Meta:
        model = Transfer
        fields = [
            'seller_email',
            'buyer_email',
            'parcel_no',
            'amount',
            'file_upload'
        ]


class SubdivisionForm(forms.ModelForm):
    class Meta:
        model = Subdivision
        fields = [
            'email',
            'parcel_no',
            'subdivision_date',
            'reason',
        ]
