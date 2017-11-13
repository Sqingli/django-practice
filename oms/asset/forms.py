from django import forms
 
class LoginForm(forms.Form):
    username = forms.IntegerField()
    password = forms.IntegerField()