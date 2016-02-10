from django import forms

class ContactUsForm(forms.Form):
    title = forms.CharField(required=True)
    message = forms.CharField(required=True)