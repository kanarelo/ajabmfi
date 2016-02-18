from __future__ import unicode_literals

from django.db import models

class MetropolRiskProfile(AuditBase):
    full_name = models.CharField(max_length=50, blank=True)

    risk_profile = models.ForeignKey('risk_management.RiskProfile')
    
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'metropol_risk_profile'
        verbose_name = "Metropol Risk Profile"

    def __unicode__(self):
        return "%s in Portfolio: %s" % (self.identity, self.portfolio)

class MetropolIdentitySearch(AuditBase):
    profile = models.ForeignKey('MetropolRiskProfile')

    is_canceled = models.BooleanField(default=False)
    date_canceled = models.DateTimeField(blank=True, null=True)
    cancel_comment = models.CharField(max_length=250, blank=True, null=True)

    search_ref_number = models.CharField(unique=True, max_length=10)

    class Meta:
        db_table = 'metropol_identity_search'
        verbose_name = "Metropol Identity Search"
        verbose_name_plural = "Metropol Identity Searches"

    def __unicode__(self):
        return self.profile

class MetropolIdentitySearchResult(AuditBase):
    #Set before search, and processing
    search = models.OneToOneField('Search')

    delinquency_code = models.ForeignKey('ConfigMetropolDelinquencyCode', null=True)
    api_ref_code = models.CharField(max_length=100)

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

    class Meta:
        db_table = 'metropol_identity_search_result'
        verbose_name = "Metropol Identity Search Result"

    def __unicode__(self):
        return "Search: '%s' for %s" % (
            self.search_list.portfolio_identity.identity.identity_number, 
            self.search_list.portfolio_identity
        )

class AccountSearchResult(AuditBase):
    account_number = models.CharField(max_length=30)
    date_opened = models.DateTimeField(null=True, blank=True)
    
    search_result = models.ForeignKey('MetropolIdentitySearchResult')
    product_type = models.ForeignKey('ConfigMetropolProductType')

    original_amount = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    current_balance = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    overdue_balance = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))

    last_payment_amount = models.DecimalField(max_digits=25, decimal_places=5, default=D('0.0'))
    last_payment_date = models.DateTimeField(null=True, blank=True)
    
    delinquency_code = models.ForeignKey('ConfigMetropolDelinquencyCode', null=True)
    days_in_arrears  = models.IntegerField(null=True, blank=True)

    overdue_date     = models.DateTimeField(null=True, blank=True)

    submitted_by = models.CharField(max_length=100)
    loaded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'metropol_account_search_result'
        verbose_name = "Metropol Account Search Result"

