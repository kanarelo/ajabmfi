from django.conf import settings
from decimal import (Decimal as D)

import request

from .models import *

METROPOL_PORT = 80

ROOT_URL =  "https://api.metropol.co.ke"
FULL_URL = "%s:%s" % (ROOT_URL, METROPOL_PORT)

IDENTITY_ENDPOINT = "/identity/verify/"
DELINQUENCY_STATUS_ENDPOINT = "/delinquency/status"
SCORE_CONSUMER_ENDPOINT = "/identity/verify/"
REPORT_PDF_ENDPOINT = "/identity/verify/"
REPORT_JSON_ENDPOINT = "/identity/verify/"
IDENTITY_SCRUB_ENDPOINT = "/identity/scrub/"

ENDPOINTS = dict(
    DELINQUENCY_STATUS="%s%s" % (FULL_URL, DELINQUENCY_STATUS_ENDPOINT),
    SCORE_CONSUMER="%s%s" % (FULL_URL, SCORE_CONSUMER_ENDPOINT),
    IDENTITY_SCRUB="%s%s" % (FULL_URL, IDENTITY_SCRUB_ENDPOINT),
    REPORT_JSON="%s%s" % (FULL_URL, REPORT_JSON_ENDPOINT),
    REPORT_PDF="%s%s" % (FULL_URL, REPORT_PDF_ENDPOINT),
    IDENTITY="%s%s" % (FULL_URL, IDENTITY_ENDPOINT),
)

GUARANTOR_GROUP = "LGT_001"
WATCHLIST_GROUP = "LGT_002"
CONSOLIDATION_GROUP = "LGT_003"

PERSONAL = "PT_001"
BUSINESS = "PT_002"
GROUP    = "PT_003"

def screen_loan_account_risk(loan_account):
    if not loan_amount:
        term = loan_account.terms.latest('created_at')
        loan_amount = term.loan_amount

    if loan_profile.profile_type.code in (PERSONAL, BUSINESS):
        the_profile = loan_profile.profile
        identity_type = the_profile.identity_type
        identity_number = the_profile.identity_number
    elif loan_profile.profile_type.code == GROUP:
        PROFILE_ACTIVE = "PS_001"

        the_profile = loan_profile.profile

        if the_profile.last_group_status.code == PROFILE_ACTIVE:
            for member in the_profile.members.all():
                if member.member_individual:
                    report = pull_report(
                        identity_type, 
                        identity_number,
                        report_type=report_type,
                        report_reason=report_reason,
                        user=user,
                        loan_amount=loan_amount
                    )
                elif member.member_business:
                    report = pull_report(
                        identity_type, 
                        identity_number,
                        report_type=report_type,
                        report_reason=report_reason,
                        user=user,
                        loan_amount=loan_amount
                    )
                elif member.member_group:
                    report = pull_report(
                        identity_type, 
                        identity_number,
                        report_type=report_type,
                        report_reason=report_reason,
                        user=user,
                        loan_amount=loan_amount
                    )

def pull_report(
    identity_type, 
    identity_number, 
    report_type=IDENTITY, 
    report_reason=NEW_CREDIT, 
    user=None, 
    loan_amount=None
):
    headers = {
        "Content-Type": "application/json",
        "X-METROPOL-REST-API-KEY": "DKKEIE3CKGPAIRJVN495JFJAJ",
        "X-METROPOL-REST-API-TIMESTAMP": "20140708175839987843",
        "X-METROPOL-REST-API-HASH": "6b4412c63b19cd86e9939c43d115x961ef4357698da42f984287e6d0029c5671",
    }

    with db_transaction.atomic():
        data = {
            "report_type": IDENTITY,
            "identity_type": identity_type,
            "identity_number": identity_number, 
        }
        
        if not MetropolRiskProfile.objects.filter(
            identity_type=identity_type,
            identity_number=identity_number
        ).exists():
            m_risk_profile = MetropolRiskProfile.objects.create(
                identity_type=identity_type,
                identity_number=identity_number
                loan_profile=loan_profile,
                created_at=timezone.now(),
                created_by=user,
            )
        else:
            m_risk_profile = MetropolRiskProfile.objects.get(
                identity_type=identity_type,
                identity_number=identity_number
            )

        REPORT_TYPE_ENDPOINT = ENDPOINTS.get(report_type)

        m_risk_profile.save()

        if report_type == IDENTITY:
            data["loan_amount"] = loan_amount
            json = request.post(REPORT_TYPE_ENDPOINT, headers=headers, data=data).json()

            m_risk_profile.first_name = json['first_name']
            m_risk_profile.other_name = json['other_name']
            m_risk_profile.last_name = json['last_name']
            
            m_risk_profile.gender = json['gender']
            m_risk_profile.dob = json['dob']
            m_risk_profile.dod = json['dod']
            
            m_risk_profile.is_verified = True

        elif report_type == DELINQUENCY_STATUS:
            data["loan_amount"] = loan_amount
            json = request.post(REPORT_TYPE_ENDPOINT, headers=headers, data=data).json()

            m_risk_profile.delinquency_status = json['delinquency_code']

        elif report_type == REPORT_PDF:
            json = request.post(REPORT_TYPE_ENDPOINT, headers=headers, data=data).json()
            
            m_risk_profile.credit_score = json['credit_score']

        elif report_type == REPORT_JSON:
            json = request.post(REPORT_TYPE_ENDPOINT, headers=headers, data=data).json()
            
            m_risk_profile.delinquency_status = json['delinquency_code']

        elif report_type == SCORE_CONSUMER:
            json = request.post(REPORT_TYPE_ENDPOINT, headers=headers, data=data).json()
            
            m_risk_profile.delinquency_status = json['credit_score']

        elif report_type == IDENTITY_SCRUB:
            json = request.post(REPORT_TYPE_ENDPOINT, headers=headers, data=data).json()

            for name in json['names']:
                r_name = RiskProfileName.objects.create(
                    risk_profile=m_risk_profile,
                    name=name
                )

            for phone in json['phone']:
                r_phone = RiskProfilePhone.objects.create(
                    risk_profile=m_risk_profile,
                    phone=phone
                )

            for email in json['email']:
                r_email = RiskProfileEmail.objects.create(
                    risk_profile=m_risk_profile,
                    email=email
                )

            for postal_address in json['postal_address']:
                r_postal_address = RiskProfilePhysicalAddress.objects.create(
                    risk_profile=m_risk_profile,
                    town=postal_address['town']
                    address=postal_address['address']
                    country=postal_address['country']
                )

            for physical_address in json['physical_address']:
                r_physical_address = RiskProfilePostalAddress.objects.create(
                    risk_profile=m_risk_profile,
                    town=physical_address['town'],
                    code=physical_address['code'],
                    number=physical_address['number'],
                    country=physical_address['country'],
                )

            for employment in json['employment']:
                r_employment = RiskProfileEmployment.objects.create(
                    risk_profile=m_risk_profile,
                    employer_name=employment['employer_name'],
                    employment_date=employment['employment_date'],
                )

            m_risk_profile.delinquency_status = json['delinquency_code']

        metropol_report = MetropolReport.objects.create(
            transaction_id=json['trx_id'],
            has_error=json['has_error'],
            api_ref_code=json['api_code'],
            api_ref_code_description=json['api_code_description'],
            identity_type=identity_type,
            identity_number=identity_number,
            report_type=report_type,
            loan_amount=json.get('loan_amount', D('0')),
            report_reason=report_reason,
        )

        m_risk_profile.identity_type = json['identity_type']
        m_risk_profile.identity_number = json['identity_number']

        m_risk_profile.last_report = metropol_report
        m_risk_profile.last_report_date = timezone.now()
        m_risk_profile.save()

        return metropol_report
