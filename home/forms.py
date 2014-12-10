from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': "form-control",
               'required': 'True'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': "form-control",
               'required': 'True'}))
