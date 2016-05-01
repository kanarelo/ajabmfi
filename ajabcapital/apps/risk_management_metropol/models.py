from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

IDENTITY_NOT_FOUND = "001"
NO_ACCOUNT_INFORMATION = "002"
NO_DELINQUENCY = "003"
CURRENTLY_DELINQUENT = "004"
HISTORICAL_DELINQUENCY = "005"
DELINQUENCY_CODES = (
    (IDENTITY_NOT_FOUND, "Identity not found"),
    (NO_ACCOUNT_INFORMATION, "No account information"),
    (NO_DELINQUENCY, "No delinquency"),
    (CURRENTLY_DELINQUENT, "Currently delinquent True"),
    (HISTORICAL_DELINQUENCY, "Historical delinquency True"),
)

IDENTITY = 1
DELINQUENCY_STATUS = 2
SCORE_CONSUMER = 3
REPORT_PDF = 4
REPORT_JSON = 5
IDENTITY_SCRUB = 6
REPORT_TYPES = (
    (IDENTITY, "Identity Verification"),
    (DELINQUENCY_STATUS, "Delinquency Report"),
    (SCORE_CONSUMER, "Check Credit Score"),
    (REPORT_PDF, "Report (PDF)"),
    (REPORT_JSON, "Report (JSON)"),
    (IDENTITY_SCRUB, "Identity Scrub"),
)

NEW_CREDIT = 1
REVIEW_OF_CREDIT = 2
VERIFY_CUSTOMER = 3
DIRECT_CUSTOMER = 4
REPORT_REASON = (
    (NEW_CREDIT, "New Credit Application"),
    (REVIEW_OF_CREDIT, "Review of Existing Credit"),
    (VERIFY_CUSTOMER, "Verify Customer Details"),
    (DIRECT_CUSTOMER, "Direct Customer Request"),
)

NATIONAL_ID = "001"
PASSPORT_NUMBER = "002"
SERVICE_ID = "003"
ALIEN_REGISTRATION = "004"
BUSINESS_REGISTRATION = "005"
IDENTITY_TYPES = (
    (NATIONAL_ID, "National ID"),
    (PASSPORT_NUMBER, "Passport"),
    (SERVICE_ID, "Service ID"),
    (ALIEN_REGISTRATION, "Alien Registration"),
    (BUSINESS_REGISTRATION, "Company/Business Registration"),
)

class MetropolReport(AuditBase):
    transaction_id = models.CharField(max_length=50, null=True)

    has_error = models.BooleanField(default=False)

    identity_type = models.CharField(max_length=4, choices=IDENTITY_TYPES)
    identity_number = models.CharField(max_length=40)

    loan_amount = models.DecimalField(max_digits=22, decimal_places=5)

    report_type = models.IntegerField(choices=REPORT_TYPES)
    report_reason = models.IntegerField(choices=REPORT_REASON)

    api_ref_code = models.CharField(max_length=50)
    api_ref_code_description = models.CharField(max_length=150)

    pdf_report = models.FileField(upload_to="risk/reports/pdf/metropol")

    class Meta:
        db_table = "metropol_report"

class MetropolRiskProfile(AuditBase):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    first_name = models.CharField(max_length=40, null=True)
    other_name = models.CharField(max_length=40, null=True)
    last_name  = models.CharField(max_length=40, null=True)

    phone = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)

    loan_profile = models.ForeignKey('loan.LoanProfile')

    identity_type = models.CharField(max_length=4, choices=IDENTITY_TYPES, null=True)
    identity_number = models.CharField(max_length=40, null=True)

    is_verified = models.BooleanField(default=False)
    
    gender = models.CharField(max_length=1, choices=GENDER, null=True)

    dob = models.DateTimeField(null=True)
    dod = models.DateTimeField(null=True)

    delinquency_status = models.CharField(max_length=4, choices=DELINQUENCY_CODES, null=True)
    is_guarantor = models.BooleanField(default=False)
    has_fraud = models.BooleanField(default=False)
    credit_score  = models.IntegerField(null=True)

    credit_app_12 = models.IntegerField(default=0, null=True)
    credit_app_6  = models.IntegerField(default=0, null=True)
    credit_app_3  = models.IntegerField(default=0, null=True)
    
    enquiries_12 = models.IntegerField(default=0, null=True)
    enquiries_6  = models.IntegerField(default=0, null=True)
    enquiries_3  = models.IntegerField(default=0, null=True)
    
    bounced_cheques_12 = models.IntegerField(default=0, null=True)
    bounced_cheques_6  = models.IntegerField(default=0, null=True)
    bounced_cheques_3  = models.IntegerField(default=0, null=True)

    bank_history_npa = models.IntegerField(default=0, null=True)
    bank_current_npa = models.IntegerField(default=0, null=True)
    bank_performing = models.IntegerField(default=0, null=True)

    other_history_npa = models.IntegerField(default=0, null=True)
    other_current_npa = models.IntegerField(default=0, null=True)
    other_performing = models.IntegerField(default=0, null=True)

    last_report = models.ForeignKey('MetropolReport', null=True)
    last_report_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "metropol_risk_profile"
        verbose_name = "Metropol Risk Profile"

    def __unicode__(self):
        return self.identity_number

class MetropolAccountDetail(AuditBase):
    PRODUCT_TYPES = (
        ("1", "Unknown"),
        ("2", "Current Account"),
        ("3", "Loan Account"),
        ("4", "Credit Card"),
        ("5", "Line of Credit"),
        ("6", "Revolving Credit"),
        ("7", "Overdraft"),
        ("8", "Credit Card"),
        ("9", "Business Working Capital"),
        ("10", "Business Expansion Loan"),
        ("11", "Mortgage"),
        ("12", "Asset Finance Loan"),
        ("13", "Trade Finance Facility"),
        ("14", "Personal Loan"),
        ("18", "Mobile Banking Loan"),
        ("19", "Other")
    )

    risk_profile = models.ForeignKey('MetropolRiskProfile')

    account_number = models.CharField(max_length=30)
    product_type = models.CharField(max_length=2, choices=PRODUCT_TYPES)

    original_amount = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    current_balance = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    overdue_balance = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    overdue_date = models.DateTimeField(null=True, blank=True)

    last_payment_amount = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    last_payment_date = models.DateTimeField(null=True, blank=True)
    
    delinquency_status = models.CharField(max_length=4, choices=DELINQUENCY_CODES)
    days_in_arrears  = models.IntegerField(null=True, blank=True)

    is_your_account = models.NullBooleanField()
    date_opened = models.DateTimeField(null=True, blank=True)

    loaded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'metropol_account_detail'
        verbose_name = "Metropol Account Detail"

class RiskProfilePhone(AuditBase):
    risk_profile = models.ForeignKey('MetropolRiskProfile')

    phone = models.CharField(max_length=100)

    class Meta:
        db_table = "risk_profile_phone"
        verbose_name = "Metropol Profile Phone"

class RiskProfileEmail(AuditBase):
    risk_profile = models.ForeignKey('MetropolRiskProfile')

    email = models.EmailField()

    class Meta:
        db_table = "risk_profile_email"
        verbose_name = "Metropol Profile Phone"

class RiskProfileName(AuditBase):
    risk_profile = models.ForeignKey('MetropolRiskProfile')

    name = models.CharField(max_length=100)

    class Meta:
        db_table = "risk_profile_name"
        verbose_name = "Metropol Profile Phone"

class RiskProfilePhysicalAddress(AuditBase):
    risk_profile = models.ForeignKey('MetropolRiskProfile')

    town = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = "risk_profile_physical_address"
        verbose_name = "Metropol Profile Physical Address"

class RiskProfilePostalAddress(AuditBase):
    risk_profile = models.ForeignKey('MetropolRiskProfile')

    town = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = "risk_profile_postal_address"
        verbose_name = "Metropol Profile Postal Address"

class RiskProfileEmployment(AuditBase):
    risk_profile = models.ForeignKey('MetropolRiskProfile')

    employer_name = models.CharField(max_length=30, null=True)
    employment_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "risk_profile_employment"
        verbose_name = "Metropol Profile Employment"
