from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-label'}))
    password = forms.CharField(label='Password', max_length=20, required=True, widget=forms.PasswordInput(attrs={'class': 'form-label'}))
