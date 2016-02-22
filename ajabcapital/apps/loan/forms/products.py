from django import forms

from decimal import Decimal as D

from ajabcapital.apps.core.models import ConfigCurrency
from ..models import *

class ProductForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(attrs=dict(rows=6)))
    is_active = forms.BooleanField(required=False)

    loan_type = forms.ModelChoiceField(queryset=[], to_field_name="code", empty_label="(select one)")

    is_revolving_facility = forms.BooleanField(required=False)
    
    default_repayment_period = forms.IntegerField(label="Repayment Period", max_value=1000, min_value=0)
    default_repayment_period_unit = forms.ModelChoiceField(label="", queryset=[], to_field_name="code", empty_label="(select one)")
    default_repayment_frequency = forms.ModelChoiceField(label="Frequency", queryset=[], to_field_name="code", empty_label="(select one)")

    has_repayment_grace_period = forms.BooleanField(label="Has Grace Period", required=False)
    default_repayment_grace_period = forms.IntegerField(label="Grace Period", 
        max_value=100, min_value=0, required=False)
    default_repayment_grace_period_unit = forms.ModelChoiceField(label="", 
        queryset=[], to_field_name="code", empty_label="(select one)")
    repayment_grace_period_type = forms.ModelChoiceField(label="Grace Period Type", queryset=[], 
        to_field_name="code", empty_label="(select one)", required=False)

    amount_currency = forms.ModelChoiceField(label="Currency", queryset=[], to_field_name="code", empty_label="(select one)")
    default_amount = forms.DecimalField(decimal_places=2, max_digits=16, min_value=D('0.0'))
    min_amount = forms.DecimalField(decimal_places=2, max_digits=16, min_value=D('0.0'))
    max_amount = forms.DecimalField(decimal_places=2, max_digits=16, min_value=D('0.0'))

    interest_calculation_method = forms.ModelChoiceField(queryset=[], to_field_name="code", empty_label="(select one)")
    default_interest_rate = forms.DecimalField(decimal_places=2, max_digits=4, min_value=D('0.0'))
    min_interest_rate = forms.DecimalField(decimal_places=2, max_digits=4, min_value=D('0.0'))
    max_interest_rate = forms.DecimalField(decimal_places=2, max_digits=4, min_value=D('0.0'))

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        period_units = ConfigLoanPeriodUnit.objects.filter(is_active=True)
        repayment_frequencies = ConfigRepaymentFrequency.objects.filter(is_active=True)
        grace_period_types = ConfigGracePeriodType.objects.filter(is_active=True)

        self.fields['default_repayment_grace_period_unit'].queryset = period_units
        self.fields['default_repayment_period_unit'].queryset = period_units
        self.fields['default_repayment_frequency'].queryset = repayment_frequencies
        self.fields['repayment_grace_period_type'].queryset = grace_period_types

        loan_types = ConfigLoanProductType.objects.filter(is_active=True)
        currencies = ConfigCurrency.objects.filter(is_active=True)
        interest_calculation_methods = ConfigInterestCalculationMethod.objects.filter(is_active=True)

        self.fields['loan_type'].queryset = loan_types
        self.fields['amount_currency'].queryset = currencies
        self.fields['interest_calculation_method'].queryset = interest_calculation_methods

    def clean(self):
        default_repayment_period = self.cleaned_data['default_repayment_period']
        default_repayment_period_unit = self.cleaned_data['default_repayment_period_unit']
        default_repayment_frequency = self.cleaned_data['default_repayment_frequency']

        default_repayment_grace_period = self.cleaned_data['default_repayment_grace_period']
        default_repayment_grace_period_unit = self.cleaned_data['default_repayment_grace_period_unit']

        return self.cleaned_data

class CreateProductForm(ProductForm):
    pass

class EditProductForm(ProductForm):
    pass