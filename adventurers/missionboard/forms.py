from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Name'})
    )

    email = forms.CharField(
        max_length=150,
        label='Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'type': 'email'})
    )

    password = forms.CharField(
        max_length=50,
        label='Password',
        widget=forms.TextInput(attrs={
            'placeholder': 'Password',
            'type': 'password'})
    )

    password2 = forms.CharField(
        max_length=50,
        label='Password',
        widget=forms.TextInput(attrs={
            'placeholder': 'Confirm Password',
            'type': 'password'})
    )


class SigninForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Name'})
    )

    password = forms.CharField(
        max_length=50,
        label='Password',
        widget=forms.TextInput(attrs={
            'placeholder': 'Password',
            'type': 'password'})
    )
