from django import forms

from .models import UserWallet




class ConfirmBookingForm(forms.Form):
    email = forms.EmailField()


class WalletCreationForm(forms.ModelForm):
    
    class Meta:
        model = UserWallet
        fields = ['bank_name', 'account_number']

class WalletEditForm(forms.ModelForm):
    class Meta:
        model = UserWallet
        fields = ['bank_name', 'account_number']