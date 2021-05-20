from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)  # help_text='Add a valid email address.')

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'username', 'gender', 'kra_pin', 'id_no',
                  'dob', 'phone', 'password1', 'password2',)
        # fields = '__all__'


# login authenticated users
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials")

    # def clean_password2(self):
    #     pw1 = self.cleaned_data.get('password1')
    #     pw2 = self.cleaned_data.get('password2')
    #     if pw1 and pw2 and pw1 == pw2:
    #         return pw2
    #     raise forms.ValidationError("passwords don't match")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
