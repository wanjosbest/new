from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=100, label='Full Name')
    email = forms.EmailField(label='Email Address')
    age = forms.IntegerField(label='Age')

    