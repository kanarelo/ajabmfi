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
        HOUR = "LP_001"
        DAY = "LP_002"
        WEEK = "LP_003"
        MONTH = "LP_004"
        YEAR = "LP_005"

        DAILY = "RF_001"
        WEEKLY = "RF_002"
        FORTNIGHTLY = "RF_003"
        MONTHLY = "RF_004"
        EVERY_TWO_MONTHS = "RF_005"
        TWICE_A_YEAR = "RF_006"
        THRICE_A_YEAR = "RF_007"
        QUARTERLY = "RF_008"
        IRREGULAR_SCHEDULE = "RF_009"
        REVOLVING = "RF_010"
        BULLET = "RF_011"
        ANNUALLY = "RF_012"

        default_repayment_period = self.cleaned_data['default_repayment_period']
        default_repayment_period_unit = self.cleaned_data['default_repayment_period_unit']
        default_repayment_frequency = self.cleaned_data['default_repayment_frequency']
        default_repayment_grace_period = self.cleaned_data['default_repayment_grace_period']
        default_repayment_grace_period_unit = self.cleaned_data['default_repayment_grace_period_unit']

        if (default_repayment_period_unit != default_repayment_grace_period_unit):
            raise forms.ValidationError(
                "Please enter the same type of unit as the repayment period "
                "for the grace period."
            )

        if (not default_repayment_period) or (
            default_repayment_period_unit.code not in (
                HOUR, DAY, WEEK, MONTH, YEAR
            )
        ):
            raise forms.ValidationError("Please enter a valid repayment period")
        else:
            if default_repayment_period_unit.code == HOUR:
                if (default_repayment_period < 24) and (default_repayment_period > 0):
                    if (default_repayment_frequency.code not in (BULLET, IRREGULAR_SCHEDULE)):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")
                #TODO: Increase the offering for hours
            elif default_repayment_period_unit.code == DAY:
                if (default_repayment_period < 7) and (default_repayment_period > 0):
                    if (default_repayment_frequency.code not in (BULLET, DAILY, IRREGULAR_SCHEDULE)):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")
            elif default_repayment_period_unit.code == WEEK:
                if (default_repayment_period < 5) and (default_repayment_period > 0):
                    if (default_repayment_frequency.code not in (
                            IRREGULAR_SCHEDULE, BULLET, DAILY, WEEKLY, FORTNIGHTLY
                        )
                    ):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")
            elif default_repayment_period_unit.code == MONTH:
                COMMON = [
                    BULLET, 
                    DAILY, 
                    WEEKLY, 
                    FORTNIGHTLY, 
                    MONTHLY, 
                    IRREGULAR_SCHEDULE
                ]

                if (default_repayment_period < 2):
                    if (default_repayment_frequency.code not in COMMON):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")
                elif (default_repayment_period < 12):
                    if (default_repayment_frequency.code not in (COMMON + [EVERY_TWO_MONTHS])):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")
                elif (default_repayment_period == 12):
                    if (default_repayment_frequency.code not in (
                        COMMON + [
                            EVERY_TWO_MONTHS, TWICE_A_YEAR, 
                            THRICE_A_YEAR, QUARTERLY
                        ]
                    )):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")

            elif default_repayment_period_unit.code == YEAR:
                if (default_repayment_period > 0):
                    if (default_repayment_frequency.code not in (
                            BULLET, DAILY, 
                            WEEKLY, FORTNIGHTLY,
                            MONTHLY, EVERY_TWO_MONTHS, 
                            TWICE_A_YEAR, THRICE_A_YEAR, 
                            QUARTERLY, IRREGULAR_SCHEDULE,
                            REVOLVING, ANNUALLY
                        )
                    ):
                        raise forms.ValidationError("Frequency invalid: Choose Bullet")

        return self.cleaned_data

class CreateProductForm(ProductForm):
    pass

class EditProductForm(ProductForm):
    pass