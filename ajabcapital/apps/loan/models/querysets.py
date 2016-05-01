from __future__ import unicode_literals

from django.db import models
from django.db.models import Q, Sum, F

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class LoanProfileQueryset(models.QuerySet):
    def credit_limit_gt(self, lower_bound):
        return self.filter(credit_limit__gt=lower_bound)

    def credit_limit_lt(self, upper_bound):
        return self.filter(credit_limit__lt=upper_bound)

    def individual_profiles(self):
        return self.filter(individual_profile__isnull=False)

    def women_profiles(self):
        FEMALE = 0
        
        return self.all().filter(
            individual_profile__gender=FEMALE
        )

    def men_profiles(self):
        MALE = 1

        return self.all().filter(
            individual_profile__gender=MALE
        )

    def business_profiles(self):
        return self.filter(business_profile__isnull=False)

    def group_profiles(self):
        return self.filter(group_profile__isnull=False)

class LoanProductQueryset(models.QuerySet):
    PRINCIPAL_GRACE_PERIOD = "GP_001"
    FULL_GRACE_PERIOD = "GP_002"

    FLAT_INTEREST = "CM_002"
    DECLINING_INTEREST = "CM_001"
    DECLINING_INTEREST_EI = "CM_003"

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
        return self.filter(Q(interest_calculation_method__code=FLAT_INTEREST))

    def declining_interest(self):
        return self.filter(Q(interest_calculation_method__code=DECLINING_INTEREST))

    def declining_interest_equal_installments(self):
        return self.filter(Q(interest_calculation_method__code=DECLINING_INTEREST_EI))

    def principal_grace_period(self):
        return self.filter(Q(repayment_grace_period_type__code=PRINCIPAL_GRACE_PERIOD))

    def full_grace_period(self):
        return self.filter(Q(repayment_grace_period_type__code=FULL_GRACE_PERIOD))

class LoanAccountQuerySet(models.QuerySet):
    #origination
    PROCESSING = "AS_011"
    APPLICATION = "AS_010"
    APPRAISAL = "AS_009"
    UNDERWRITING = "AS_008"
    DISBURSEMENT = "AS_007"

    #repayment/servicing
    PERFORMING = "AS_006"
    OUTSTANDING = "AS_002"
    REPERFORMING = "AS_012"

    #NPLs
    DELINQUENT = "AS_014"
    NON_PERFORMING = "AS_001"
    
    #closed
    DISPUTED = "AS_015"
    RESTRUCTURED = "AS_003"
    WRITE_OFF = "AS_004"

    #close
    FULLY_PAID = "AS_005"
    CLOSED = "AS_013"
    
    #Repayment Frequencies...
    RF_EVERY_DAY = "RF_001"
    RF_EVERY_WEEK = "RF_002"
    RF_EVERY_2_WEEKS = "RF_003"
    RF_EVERY_MONTH = "RF_004"
    RF_EVERY_2_MONTHS = "RF_005"
    RF_EVERY_3_MONTHS = "RF_006"
    RF_EVERY_4_MONTHS = "RF_007"
    RF_EVERY_6_MONTHS = "RF_008"
    RF_EVERY_12_MONTHS = "RF_009"
    RF_REVOLVING = "RF_010"
    RF_BULLET = "RF_011"

    #status
    def active(self):
        accounts = self.filter(
            Q(date_disbursed__isnull=False) & (
                Q(current_account_status__code=self.PERFORMING)|
                Q(current_account_status__code=self.OUTSTANDING)|
                Q(current_account_status__code=self.REPERFORMING)|
                Q(current_account_status__code=self.NON_PERFORMING)
            )
        )
        
        return accounts

    def outstanding(self):
        return self.filter(
            Q(current_account_status__code=self.OUTSTANDING)
        )

    def closed(self):
        return self.filter(
            Q(current_account_status__code=self.RESTRUCTURED)|
            Q(current_account_status__code=self.FULLY_PAID)|
            Q(current_account_status__code=self.WRITE_OFF)|
            Q(current_account_status__code=self.CLOSED)
        )

    def performing(self):
        accounts = self.filter(
            Q(date_disbursed__isnull=False) & (
                Q(current_account_status__code=self.PERFORMING)|
                Q(current_account_status__code=self.OUTSTANDING)
            )
        )
        return accounts

    def non_performing(self):
        return self.filter(
            Q(current_account_status__code=self.REPERFORMING)|
            Q(current_account_status__code=self.NON_PERFORMING)
        )

    def reperfoming(self):
        return self.filter(
            Q(current_account_status__code=self.REPERFORMING)
        )

    def in_processing(self):
        return self.filter(
            Q(current_account_status__code=self.PROCESSING)|
            Q(current_account_status__code=self.APPRAISAL)|
            Q(current_account_status__code=self.UNDERWRITING)|
            Q(current_account_status__code=self.DISBURSEMENT)
        )

    def in_origination(self):
        return self.filter(
            Q(current_account_status__code=self.PROCESSING)|
            Q(current_account_status__code=self.APPLICATION)|
            Q(current_account_status__code=self.APPRAISAL)|
            Q(current_account_status__code=self.UNDERWRITING)|
            Q(current_account_status__code=self.DISBURSEMENT)
        )

    def in_disbursement(self):
        return self.filter(
            Q(current_account_status__code=self.DISBURSEMENT)
        )

    def in_repayment(self):
        return self.filter(
            Q(current_account_status__code=self.PROCESSING)|
            Q(current_account_status__code=self.APPLICATION)|
            Q(current_account_status__code=self.APPRAISAL)
        )

    def disputed(self):
        return self.filter(Q(current_account_status__code=self.DISPUTED))

    def write_offs(self):
        return self.filter(Q(current_account_status__code=self.WRITE_OFF))

    def term_loans(self):
        return self.filter(Q(term__loan_account__isnull=False))
        
    def restructured_loans(self):
        return self.term_loans().filter(
            Q(current_account_status__code=self.RESTRUCTURED) &
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
        return self.filter(Q(term__repayment_frequency__code=RF_BULLET))

    def revolving_loans(self):
        return self.filter(Q(term__repayment_frequency__code=RF_REVOLVING))

    def annual_accruing(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_12_MONTHS))

    def halfly_accruing(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_6_MONTHS))

    def quaterly_accruing(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_4_MONTHS))

    def three_month_accruing(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_3_MONTHS))

    def two_month_accuring(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_2_MONTHS))

    def monthly_accuring(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_MONTH))

    def fortnighly_accuring(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_2_WEEKS))

    def weekly_accuring(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_WEEK))

    def everyday_accuring(self):
        return self.filter(Q(term__repayment_frequency__code=RF_EVERY_DAY))

    #-------------- by accrual type
    def accrual_loans(self):
        return self.performing()

    def non_accrual_loans(self):
        return self.non_performing()

    def risk_classified(self, risk_classification_code):
        return self.filter(
            current_risk_classification__code=risk_classification_code
        )