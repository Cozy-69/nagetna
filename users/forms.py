from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import Account


class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email.")
    birth_day = forms.DateField()
    class Meta:
        model = Account
        fields = ['email', 'username', 'birth_day', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email: {email} is already in use")


class AccountAuthenticateForm(forms.Form):
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)





class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("username","email","birth_day","bio","profile_image", "hide_email", "hide_birth_day")
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email: {email} is already in use")

    # def save(self, commit=True):
    #     o_account = Account.objects.get(email=self.cleaned_data['email'].lower())
    #     account = super(AccountEditForm, self).save(commit=False)
    #     account.username = self.cleaned_data["username"] 
    #     account.email = self.cleaned_data["email"] 
    #     account.birth_day = o_account.birth_day
    #     account.bio = self.cleaned_data["bio"] 
    #     account.profile_image = self.cleaned_data["profile_image"] 
    #     account.hide_email = self.cleaned_data["hide_email"] 
    #     account.hide_birth_day = self.cleaned_data["hide_birth_day"] 
    #     if commit:
    #         account.save()

    #     return account
    
    