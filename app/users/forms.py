from django import forms


class UserCreateForm(forms.Form):
    public_key = forms.CharField()
