from django import forms
from .models import Ownership


class OwnershipForm(forms.ModelForm):

    class Meta:
        model = Ownership
        fields = '__all__'


# multiple files
class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    message = forms.CharField(widget=forms.Textarea)
