from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class LoanProfileQueryset(models.QuerySet):
    def credit_limit_gt(self, lower_bound):
        return self.filter(credit_limit__gt=lower_bound)

    def credit_limit_lt(self, upper_bound):
        return self.filter(credit_limit__lt=upper_bound)

    def individual_profiles(self):
        return self.filter(individual_profile__isnull=False)

    def business_profiles(self):
        return self.filter(business_profile__isnull=False)

    def group_profiles(self):
        return self.filter(group_profile__isnull=False)

class LoanProductQueryset(models.QuerySet):
    def active(self):
        return self.filter(Q(is_active=True))

    def inactive(self):
        return self.filter(Q(is_active=False))

    #-------------
    def ussd(self):
        return self.filter(Q(channel__code="CHN_001"))

    def smartphone(self):
        return self.filter(Q(channel__code="CHN_002"))

    def mobile(self):
        return self.filter(Q(channel__code="CHN_001") | Q(channel__code="CHN_002"))

    def web(self):
        return self.filter(Q(channel__code="CHN_003"))

    def chatbot(self):
        return self.filter(Q(channel__code="CHN_004"))

    def multi_channel(self):
        return self.filter(Q(channel__code="CHN_005"))

    #------------- funds
    def syndicated(self):
        return self.filter(Q(fund__fund_type__code=""))

    def bilateral(self):
        return self.filter(Q(fund__fund_type__code=""))

    #-------------
    def personal_loans(self):
        return self.filter(Q(product_type__code="LT_001"))

    def business_loans(self):
        return self.filter(Q(product_type__code="LT_002"))

    def group_loans(self):
        return self.filter(Q(product_type__code="LT_003"))

    #-------------
    def kes_loans(self):
        return self.filter(Q(amount_currency__code="KES"))

    def usd_loans(self):
        return self.filter(Q(amount_currency__code="USD"))

    def flat_interest(self):
        return self.filter(Q(interest_calculation_method__code="CM_002"))

    def declining_interest(self):
        return self.filter(Q(interest_calculation_method__code="CM_001"))

    def principal_grace_period(self):
        return self.filter(Q(repayment_grace_period_type__code="GP_001"))

    def full_grace_period(self):
        return self.filter(Q(repayment_grace_period_type__code="GP_002"))

class LoanAccountQuerySet(models.QuerySet):
    #origination
    PROCESSING = "AS_011"
    APPLICATION = "AS_010"
    APPRAISAL = "AS_009"
    UNDERWRITING = "AS_008"
    DISBURSEMENT = "AS_007"

    #repayment
    PERFORMING = "AS_006"
    OUTSTANDING = "AS_002"
    DELINQUENT = "AS_014"
    REPERFORMING = "AS_012"
    NON_PERFORMING = "AS_001"
    
    #closed
    DISPUTED = "AS_015"
    RESTRUCTURED = "AS_003"
    FULLY_PAID = "AS_005"
    WRITE_OFF = "AS_004"
    CLOSED = "AS_013"

    #status
    def active(self):
        accounts = self.filter(
            Q(last_account_status__code=self.REPERFORMING)|
            Q(last_account_status__code=self.PERFORMING)|
            Q(last_account_status__code=self.OUTSTANDING)
        )
        
        return accounts

    def closed(self):
        return self.filter(
            Q(last_account_status__code=self.RESTRUCTURED)|
            Q(last_account_status__code=self.FULLY_PAID)|
            Q(last_account_status__code=self.WRITE_OFF)|
            Q(last_account_status__code=self.CLOSED)
        )

    def performing(self):
        return self.filter(
            Q(last_account_status__code=self.PERFORMING)|
            Q(last_account_status__code=self.OUTSTANDING)
        )

    def outstanding(self):
        return self.filter(
            Q(last_account_status__code=self.OUTSTANDING)
        )

    def non_performing(self):
        return self.filter(
            last_account_status__code=self.DISPUTED
        )

    def in_processing(self):
        return self.filter(
            Q(last_account_status__code=self.PROCESSING)|
            Q(last_account_status__code=self.APPRAISAL)|
            Q(last_account_status__code=self.UNDERWRITING)|
            Q(last_account_status__code=self.DISBURSEMENT)
        )

    def in_origination(self):
        return self.filter(
            Q(last_account_status__code=self.PROCESSING)|
            Q(last_account_status__code=self.APPLICATION)|
            Q(last_account_status__code=self.APPRAISAL)|
            Q(last_account_status__code=self.UNDERWRITING)|
            Q(last_account_status__code=self.DISBURSEMENT)
        )

    def in_repayment(self):
        return self.filter(
            Q(last_account_status__code=self.PROCESSING)|
            Q(last_account_status__code=self.APPLICATION)|
            Q(last_account_status__code=self.APPRAISAL)
        )

    def disputed(self):
        return self.filter(Q(last_account_status__code=self.DISPUTED))

    def write_offs(self):
        return self.filter(Q(last_account_status__code=self.WRITE_OFF))

    def term_loans(self):
        return self.filter(Q(term__loan_account__isnull=False))

    def restructured_loans(self):
        return self.term_loans().filter(
            Q(last_account_status__code=self.RESTRUCTURED) &
            Q(term__terms_restructured__isnull=False) &
            Q(term__terms_restructured_date__isnull=False)
        ) 

    def grace_period_loans(self):
        return self.filter(
            Q(term__grace_period__isnull=False) &
            Q(term__grace_period_unit__isnull=False)
        )

    #-------------- repayment_frequencies
    def bullet_loans(self):
        return self.filter(Q(repayment_frequency__code="RF_011"))

    def revolving_loans(self):
        return self.filter(Q(repayment_frequency__code="RF_010"))

    def annual_accruing(self):
        return self.filter(Q(repayment_frequency__code="RF_009"))

    def halfly_accruing(self):
        return self.filter(Q(repayment_frequency__code="RF_008"))

    def quaterly_accruing(self):
        return self.filter(Q(repayment_frequency__code="RF_007"))

    def three_month_accruing(self):
        return self.filter(Q(repayment_frequency__code="RF_006"))

    def two_month_accuring(self):
        return self.filter(Q(repayment_frequency__code="RF_005"))

    def monthly_accuring(self):
        return self.filter(Q(repayment_frequency__code="RF_004"))

    def fortnighly_accuring(self):
        return self.filter(Q(repayment_frequency__code="RF_003"))

    def weekly_accuring(self):
        return self.filter(Q(repayment_frequency__code="RF_002"))

    def everyday_accuring(self):
        return self.filter(Q(repayment_frequency__code="RF_001"))
