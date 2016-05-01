import uuid
import random
import math
import names
import radar
import logging

from calendar import monthrange
from datetime import timedelta, datetime
from dateutil import relativedelta
from decimal  import Decimal as D

from django.db import transaction as db_transaction
from django.db.models import Q, Sum, F
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from ..models import *
from ..utils import *
from ...core.utils import *
from ...core.facades import *

INITIAL = D('0.0')

#Loan COA Ledger Balances
#---------------------------
def get_chart_of_accounts_balances(loan_account=None, filter_accounts=[]):
    #Get the chart of accounts
    with db_transaction.atomic():
        chart_of_accounts = LoanChartOfAccounts.objects.filter(is_active=True)

        accounts = {}

        for account in chart_of_accounts:
            if (account.name in filter_accounts):
                ledger_account = LedgerAccount.objects.get(ledger_code=account.code)
                accounts[account.name] = dict(
                    account=ledger_account, 
                    balance=get_ledger_account_balance(ledger_account, product_account=loan_account)
                )

        return accounts

def get_loan_account_coa_balances(loan_account, filter_accounts=[]):
    return get_chart_of_accounts_balances(loan_account=loan_account, filter_accounts=filter_accounts)

#---------------------------
def get_loan_account_current_balance(loan_account):
    accounts = get_loan_account_coa_balances(
        loan_account, filter_accounts=['loan_portfolio_control_account']
    )
    return accounts['loan_portfolio_control_account']['balance']

def get_repayment_due_on_loan_account(loan_account):
    accruals_due_on_account  = get_accruals_due_on_loan_account(loan_account)
    principal_due_on_account = get_principal_due_on_loan_account(loan_account)

    return (
        INITIAL + 
        accruals_due_on_account + 
        principal_due_on_account 
    )

def get_accruals_due_on_loan_account(loan_account):
    accounts = get_loan_account_coa_balances(
        loan_account, filter_accounts=[
            'loan_interest_income_receivable_account',
            'loan_fee_income_receivable_account',
            'loan_penalty_income_receivable_account'
        ]
    )
    return (
        accounts['loan_fee_income_receivable_account']['balance'] +
        accounts['loan_interest_income_receivable_account']['balance'] +
        accounts['loan_penalty_income_receivable_account']['balance'] 
    )

def get_fees_due_on_loan_account(loan_account):
    accounts = get_loan_account_coa_balances(
        loan_account, filter_accounts=['loan_fee_income_receivable_account']
    )
    return accounts['loan_fee_income_receivable_account']['balance']

def get_penalties_due_on_loan_account(loan_account):
    accounts = get_loan_account_coa_balances(
        loan_account, filter_accounts=['loan_penalty_income_receivable_account']
    )
    return accounts['loan_penalty_income_receivable_account']['balance']

def get_interest_due_on_loan_account(loan_account):
    accounts = get_loan_account_coa_balances(
        loan_account, filter_accounts=['loan_interest_income_receivable_account']
    )
    return accounts['loan_interest_income_receivable_account']['balance']

def get_principal_due_on_loan_account(loan_account):
    return 

#--------------------------------------
ICM_FLAT = "CM_001" 
ICM_DECLINING_BALANCE = "CM_002" 
ICM_DECLINING_BALANCE_EQUAL = "CM_003" 

DAYS_IN_A_YEAR  = D('365.25')
DAYS_IN_A_WEEK  = D('7')
DAYS_IN_A_MONTH = (DAYS_IN_A_YEAR / 12)

LP_HOUR  = "LP_001"
LP_DAY   = "LP_002"
LP_WEEK  = "LP_003"
LP_MONTH = "LP_004"
LP_YEAR  = "LP_005"

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

RM_TERM = "TRM_001"
RM_REVOLVING = "TRM_002"
RM_BULLET = "TRM_003"

PRINCIPAL_GRACE_PERIOD = "GP_001"
FULL_GRACE_PERIOD = "GP_002"

class InstallmentSchedule(object):
    class Installment(object):
        def __init__(self, 
            installment_index=0, 
            
            installment_date=None,
            principal_due=0,
            interest_due=0,
            fees_due=0,
            penalties_due=0,
            installment_due=0,
            
            date_paid=0,
            principal_paid=0,
            interest_paid=0,
            fees_paid=0,
            penalties_paid=0,
            installment_paid=0,
            
            loan_balance=0,
            status=None
        ):
            self.installment_index = installment_index
            self.installment_date  = installment_date

            self.principal_due = principal_due
            self.interest_due = interest_due
            self.penalties_due = penalties_due
            self.fees_due = fees_due
            self.installment_due = installment_due

            self.principal_paid = principal_paid
            self.interest_paid = interest_paid
            self.penalties_paid = penalties_paid
            self.fees_paid = fees_paid
            self.installment_paid = installment_paid

            self.loan_balance = loan_balance
            self.status = status

        def __str__(self):
            return "%s\t%s |\t %.2f |\t%.2f |\t%.2f |\t%.2f | \t%.2f | \t%.2f | \t%.2f" % (
                self.installment_index,
                (self.installment_date.strftime("%d/%m/%Y")),
                D(self.principal_paid),
                D(self.interest_paid),
                D(self.installment_paid),
                D(self.principal_due),
                D(self.interest_due),
                D(self.installment_due),
                D(self.loan_balance)
            )

    def __init__(self, loan_account):
        self.date_list = []
        self.installments = []
        self.loan_account = loan_account

    def add_installment(self, *args, **kwargs):
        self.date_list.append(kwargs.get('installment_date'))
        self.installments.append(InstallmentSchedule.Installment(*args, **kwargs))

    def __str__(self):
        term = self.loan_account.terms.latest('created_at')
        product = self.loan_account.product

        repayment_period = term.repayment_period
        repayment_period_unit = term.repayment_period_unit
        repayment_frequency = term.repayment_frequency
        grace_period = term.grace_period
        grace_period_unit = term.grace_period_unit
        grace_period_type = product.repayment_grace_period_type

        _str = "\n=================================================\n"
        _str += " Loan Amount: %s \t\t\t\n" % str(term.loan_amount)
        _str += " Loan Profile: %s \t\t\t\n" % str(self.loan_account.loan_profile)
        _str += " Loan Account: %s \t\t\t\n" % self.loan_account.account_number
        _str += " Date Disbursed: %s \t\t\t\n" % self.loan_account.date_disbursed.strftime("%d/%m/%Y")
        _str += " Repayment Period: %s %s \t\t\t\n" % (repayment_period, repayment_period_unit.name)
        _str += " Repayment Frequency: %s \t\t\n" % (repayment_frequency.name)
        
        if grace_period and grace_period_unit:
            _str += " Grace period: %s %s %s \t\t\t\n" % (grace_period, grace_period_unit.name, grace_period_type.name)

        _str += " Repayment Model: %s \t\t\t\n" % (self.loan_account.product.repayment_model.name)
        _str += " Interest rate: %.2f%%/%s \t\t\t\n" % (term.interest_rate, term.interest_rate_unit)
        _str += " Interest calculation method: %s \t\t\n" % self.loan_account.product.interest_calculation_method.name
        _str += "=================================================\n\n"
        _str += "#\tDate\tPrincipal\tInterest\tTotal Paid\tPrincipal\tInterest\tTotal Due\tBalance"

        for payment in self.installments:
            _str += "\n%s" % str(payment)

        return _str

    def size(self):
        return len(self.installments)

    def get_installments(self):
        return self.installments

    def accurals_matured(self):
        for date in self.date_list:
            if (timezone.now() - date).days == 0:
                return True

        return False

def get_last_day_in_series(
    period, 
    period_unit, 
    first_date=None,
):
    last_date = None


    if period_unit:
        if period_unit.code == LP_HOUR:
            last_date = first_date + relativedelta.relativedelta(hours=period)
        elif period_unit.code == LP_DAY:
            last_date = first_date + relativedelta.relativedelta(days=period)
        elif period_unit.code == LP_WEEK:
            last_date = first_date + relativedelta.relativedelta(weeks=period)
        elif period_unit.code == LP_MONTH:
            last_date = first_date + relativedelta.relativedelta(months=period)
        elif period_unit.code == LP_YEAR:
            last_date = first_date + relativedelta.relativedelta(years=period)
        
    return last_date

def get_date_series(
    repayment_frequency, 
    first_date=None, 
    last_date=None
):
    next_date  = first_date
    
    date_series = []

    while next_date < last_date:
        if repayment_frequency.code == RF_EVERY_DAY:
            next_date = next_date + relativedelta.relativedelta(days=1)
        elif repayment_frequency.code == RF_EVERY_WEEK:
            next_date = next_date + relativedelta.relativedelta(days=7)
        elif repayment_frequency.code == RF_EVERY_2_WEEKS:
            next_date = next_date + relativedelta.relativedelta(days=14)
        elif repayment_frequency.code == RF_EVERY_MONTH:
            next_date = next_date + relativedelta.relativedelta(months=1)
        elif repayment_frequency.code == RF_EVERY_2_MONTHS:
            next_date = next_date + relativedelta.relativedelta(months=2)
        elif repayment_frequency.code == RF_EVERY_3_MONTHS:
            next_date = next_date + relativedelta.relativedelta(months=3)
        elif repayment_frequency.code == RF_EVERY_4_MONTHS:
            next_date = next_date + relativedelta.relativedelta(months=4)
        elif repayment_frequency.code == RF_EVERY_6_MONTHS:
            next_date = next_date + relativedelta.relativedelta(months=6)
        elif repayment_frequency.code == RF_EVERY_12_MONTHS:
            next_date = next_date + relativedelta.relativedelta(months=12)
        else:
            return []

        date_series.append(next_date)

    return date_series

def get_installment_dates(loan_account):
    disbursement_date = loan_account.date_disbursed
    term = loan_account.terms.latest('created_at')

    repayment_period = term.repayment_period
    repayment_period_unit = term.repayment_period_unit
    repayment_frequency = term.repayment_frequency
    repayment_model = loan_account.product.repayment_model

    last_date = get_last_day_in_series(
        repayment_period,
        repayment_period_unit,
        first_date=disbursement_date
    )

    if repayment_model.code == RM_TERM:
        return get_date_series(
            repayment_frequency,
            first_date=disbursement_date,
            last_date=last_date
        )
    elif repayment_model.code == RM_REVOLVING:
        if repayment_frequency.code == RF_REVOLVING:
            return [last_date]
    elif repayment_model.code == RM_BULLET:
        if repayment_frequency.code == RF_BULLET:
            return [last_date]

def get_loan_repayments(loan_account):
    repayments = LedgerTransaction.objects.product_account_transactions(
        product_account=loan_account.account_number
    ).loan_repayments().posted()

    return repayments

#TODO:
def get_term_installment_schedule(loan_account):
    def get_daily_interest_rate(
        interest_rate,
        interest_rate_unit, 
        days_in_the_month=DAYS_IN_A_MONTH, 
        days_in_the_year=DAYS_IN_A_YEAR
    ):
        if interest_rate_unit.code == LP_HOUR:
            return interest_rate
        elif interest_rate_unit.code == LP_WEEK:
            return interest_rate / DAYS_IN_A_WEEK
        elif interest_rate_unit.code == LP_MONTH:
            return interest_rate / days_in_the_month
        elif interest_rate_unit.code == LP_YEAR:
            return interest_rate / days_in_the_year
        
        return D('0.0')
    
    def get_grace_period_installments(
        repayment_frequency, 
        first_date=None, 
        last_date=None
    ):
        date_series = get_date_series(
            repayment_frequency, 
            first_date=first_date,
            last_date=last_date
        )
        return date_series

    def get_date_diff(date2, date1):
        delta = (date2 - date1)
        return delta.days

    term = loan_account.terms.latest('created_at')
    product = loan_account.product
    disbursement_date = loan_account.date_disbursed
    repayment_frequency = term.repayment_frequency

    #grace period
    grace_period = term.grace_period
    grace_period_unit = term.grace_period_unit
    grace_period_type = product.repayment_grace_period_type
    grace_period_installments = []
    grace_period_days = 0
    grace_period_final_day = get_last_day_in_series(
        grace_period, 
        grace_period_unit,
        first_date=disbursement_date
    )

    if grace_period_final_day:
        grace_period_days = get_date_diff(grace_period_final_day, disbursement_date)
        grace_period_installments = get_grace_period_installments(
            repayment_frequency,
            first_date=disbursement_date, 
            last_date=grace_period_final_day
        )

    #get the installment dates and initialise the schedule
    installment_dates = get_installment_dates(loan_account)
    installment_schedule = InstallmentSchedule(loan_account)
    #get the number of installments
    equal_installment = 0
    no_of_installments = D(len(installment_dates))
    no_of_installments -= D(len(grace_period_installments))
    
    #set the loan amounts and balances
    loan_amount = term.loan_amount
    loan_balance = loan_amount

    #set the interest rates
    interest_rate = term.interest_rate
    interest_rate_unit = term.interest_rate_unit
    interest_calculation_method = loan_account.product.interest_calculation_method

    percentage_interest_rate = term.interest_rate / D('100')
    daily_interest_rate = get_daily_interest_rate(percentage_interest_rate, interest_rate_unit)

    #set previous date as disbursement date, initialise `equal_installment`
    previous_date = disbursement_date

    repayments = get_loan_repayments(loan_account)

    for (i, date) in enumerate(installment_dates):
        #get the date difference between previous date and current date
        days = get_date_diff(date, previous_date)

        if (grace_period_days > 0) and ((grace_period_days - days) < 0):
            days = grace_period_days

        if interest_calculation_method.code == ICM_FLAT:
            principal_due = D(math.ceil(loan_amount / no_of_installments))
            interest_due = (loan_amount  * (daily_interest_rate * days))
        elif interest_calculation_method.code == ICM_DECLINING_BALANCE:
            principal_due = D(math.ceil(loan_amount / no_of_installments))
            interest_due = (loan_balance * (daily_interest_rate * days))
        elif interest_calculation_method.code == ICM_DECLINING_BALANCE_EQUAL:
            if not equal_installment:
                _DAYS_IN_A_MONTH = D('30.5')

                effective_interest_rate = (daily_interest_rate * _DAYS_IN_A_MONTH)

                if repayment_frequency.code == RF_EVERY_MONTH:
                    effective_interest_rate *= 1
                elif repayment_frequency.code == RF_EVERY_2_MONTHS:
                    effective_interest_rate *= 2
                elif repayment_frequency.code == RF_EVERY_3_MONTHS:
                    effective_interest_rate *= 3
                elif repayment_frequency.code == RF_EVERY_4_MONTHS:
                    effective_interest_rate *= 4
                elif repayment_frequency.code == RF_EVERY_6_MONTHS:
                    effective_interest_rate *= 6
                elif repayment_frequency.code == RF_EVERY_12_MONTHS:
                    effective_interest_rate *= 12
                else:
                    effective_interest_rate = daily_interest_rate * days

                '''
                The monthly payments formulae:
                r = installment interest rate
                n = number of installments

                a = r * ((1 + r) ^ n)
                b = ((1 + r) ^ n) - 1
                '''
                a = effective_interest_rate * ((1 + effective_interest_rate) ** no_of_installments)
                b = (((1 + effective_interest_rate) ** no_of_installments) - 1)

                equal_installment = D(math.ceil(loan_amount * (a / b)))

            interest_due  = (loan_balance * (daily_interest_rate * days))
            principal_due = (equal_installment - interest_due)

        if grace_period_days > 0:
            if grace_period_type.code == PRINCIPAL_GRACE_PERIOD:
                principal_due = D('0.0')
            elif grace_period_type.code == FULL_GRACE_PERIOD:
                principal_due = D('0.0')
                interest_due  = D('0.0')

        if (loan_balance - principal_due) > 0:
            loan_balance -= principal_due
        else:
            principal_due = loan_balance
            loan_balance = 0

        fees_due = D('0.0')
        penalties_due = D('0.0')

        try:
            repayment = repayments.get(
                last_status_date__gte=previous_date,
                last_status_date__lt=date
            )
            installment_paid = repayment.amount

            #set the interest, fees and penalties
            interest_paid = interest_due
            fees_paid = fees_due
            penalties_paid = penalties_due

            #set the principal paid
            principal_paid = installment_paid - (
                interest_paid + 
                fees_paid + 
                penalties_paid
            )

            if principal_paid <= 0:
                principal_paid = 0

        except ObjectDoesNotExist:
            repayment = None

            installment_paid = D('0.0')
            interest_paid = D('0.0')
            fees_paid = D('0.0')
            penalties_paid = D('0.0')
            principal_paid = D('0.0')

        #add installments to schedule
        installment_due = (principal_due + interest_due + fees_due + penalties_due)
        installment_schedule.add_installment(
            installment_date=date,
            installment_index=i,

            installment_paid=installment_paid,
            principal_paid=principal_paid,
            penalties_paid=penalties_paid,
            interest_paid=interest_paid,
            fees_paid=fees_paid,
            
            installment_due=installment_due,
            principal_due=principal_due,
            penalties_due=penalties_due,
            interest_due=interest_due,
            fees_due=fees_due,

            loan_balance=loan_balance,
        )

        previous_date = date
        grace_period_days -= days

    return installment_schedule
