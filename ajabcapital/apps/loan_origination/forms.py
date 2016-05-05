from django import forms

class PrequalificationForm(forms.Form):
    full_name = forms.CharField()
    age = forms.IntegerField()
    gender = forms.IntegerField()
    location = forms.CharField()
    loan_amount_range = forms.CharField()
    credit_score_range = forms.CharField()
    revenue_range = forms.CharField()
    loan_purpose = forms.CharField()