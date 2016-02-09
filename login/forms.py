from django import forms 


class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
