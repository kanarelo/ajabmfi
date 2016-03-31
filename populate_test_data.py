from django.db.models import Q, Sum, F
from django.utils import timezone

from django.db import transaction as db_transaction

from decimal import Decimal as D

import uuid
import random
import names

from calendar import monthrange
from datetime import timedelta

from ajabcapital.apps.core import utils
from ajabcapital.apps.core.models import *
from ajabcapital.apps.crm.models import *
from ajabcapital.apps.loan.models import *
from ajabcapital.apps.loan_origination.models import *

GENDERS = ['female', 'male']
EMAIL_PROVIDERS = [
    "ajabcapital", 
    "hotmail", 
    "gmail", 
    "yahoo", 
    "ymail", 
    "rmail",
]

def populate_profiles():
    def create_group_loan_profile():
        GROUPS = [
            "Turande vijana", "Mambo ville", "Komarock", "Kayole self help", "Gobika", "Samba village", 
            "Mambo Vile", "Buruburu Boys", "Ofafa Maringo", "Ofafa Jericho", "Makongeni", "Uhuru", 
            "Kaloleni", "Outering", "Makadara", "Madaraka", "Ruai", "Ruaka", "Limuru", "Carnivore", 
            "HQ", "Kibera", "Highrise", "Mbagathi", "Mpaka", "Strathmore", "Kasuku", "Gordy", 
            "Freddie", "Studio", "Hutchery", "Samosa", "dephanie marketing services", 
            "afrizone general contractors ltd", "sinopia limited", "hampton construction co. limited", 
            "konel agencies limited", "flex trading enterprises", "kalimba kenya", "central tech enterprise", 
            "blue ray technologies", "leone general supplies", "esmeralda peridot investments", 
            "africage general suppliers", "geotha general supplies", "nalex investment", 
            "kathay business enterprises", "hamptons ventures limited", "multimax enterprises limited", 
            "optimal entreprenuer", "tendakazi entrepreneurs", "rahisac business enterprise limited", 
            "kaggz designer", "evpasu enterprises", "midy enterprises limited",
            "hosana ltd", "dodoma ltd", "desky ltd", "tuskyz ltd", "xoxo ltd", "soapy news ltd",
            "sakanya ltd", "matai ltd", "mukunda ltd", "boas ltd", "noni ltd", 
            "safaricom ltd", "garden valley", "strathmore university", "sasatel", 
            "ogopa djs", "british american tobacco limited", "cooper motor corporation",
            "del monte kenya", "east african breweries", "eveready east africa", 
            "kakuzi limited", "mobius motors", "mumias sugar", "rea vipingo sisal estate", 
            "sasini tea and coffee","polymath solutions", "graycard solutions", "nieter cleaning services",
            "maxserve enterprises", "starec general supplies", "makso general merchants limited",
            "afri globe east africa ltd", "shinka limited", "stewere brands", "deal safi enterprises",
            "pinnacle multiprod ltd", "jedeve investment", "y-pen investment limited", "liton company limited",
            "wisemen business solutions", "x-pro designs & constructions limited", "dotto computer agency",
            "nevstin enterprises", "rowambu enterprises", "scoffold investments ltd", "stoneridge limited",
            "riziki julia enterprises k limited", "afri fields investment ltd", "abbigoh enterprises limited",
            "simplex africa limited", "nelken solutions kenya limited", "dondan holdings limited",
            "urim and thummim enterprises", "mariana suppliers", "egalaxy kenya limited",
            "yvette supplies and agencies", "the herbive pest services", "nawada enterprises",
        ]
        group = random.choice(GROUPS)
        group_profile = GroupProfile.objects.create(
            name="%s Group" % group,
            loan_group_type_id=random.choice((1, 2, 3)),
            last_group_status_id=random.randint(1, 3),
            last_group_status_date=timezone.now(),
            created_by_id=3
        )
        loan_group_status = GroupProfileStatus.objects.create(
            group_profile=group_profile,
            status_id=random.randint(1, 3),
            approved_by_id=3,
            created_by_id=3
        )
        loan_profile = LoanProfile.objects.create(
            group_profile=group_profile,
            credit_limit=random.choice((5000, 40000, 150000, 100000, 88000, 95000)),
            created_by_id=3,
            profile_type_id=3
        )

        return loan_profile

    def create_business_loan_profile():
        BUSINESSES = [
            "synacor ltd", "ajabworld ltd", "ajabcapital ltd", "weza tele ltd",
            "jumo world ltd", "babasuko ltd", "rock-a-fella ltd", "pesa zetu ltd",
            "doadoa ltd", "vive visuals partnership", "cabanas partnership", 
            "guranche partnership", "basnivu partnership",
            "mcdonalds ltd", "thika road mall partnership", "blueshield partnership", 
            "metropol crb partnership", "camusat ltd", "coca-cola", "kplc", "kisumu hotel", 
            "kura group ltd", "abc", "ajabpay ltd", "jozi group ltd", "asana group ltd", 
            "gogolo group ltd", "sambaza group ltd", "onfon group ltd", "digital sacco ltd", 
            "hosana ltd", "dodoma ltd", "desky ltd", "tuskyz ltd", "xoxo ltd", "soapy news ltd",
            "sakanya ltd", "matai ltd", "mukunda ltd", "boas ltd", "noni ltd", 
            "safaricom ltd", "garden valley", "strathmore university", "sasatel", 
            "ogopa djs", "british american tobacco limited", "cooper motor corporation",
            "del monte kenya", "east african breweries", "eveready east africa", 
            "kakuzi limited", "mobius motors", "mumias sugar", "rea vipingo sisal estate", 
            "sasini tea and coffee","polymath solutions", "graycard solutions", "nieter cleaning services",
            "maxserve enterprises", "starec general supplies", "makso general merchants limited",
            "afri globe east africa ltd", "shinka limited", "stewere brands", "deal safi enterprises",
            "pinnacle multiprod ltd", "jedeve investment", "y-pen investment limited", "liton company limited",
            "wisemen business solutions", "x-pro designs & constructions limited", "dotto computer agency",
            "nevstin enterprises", "rowambu enterprises", "scoffold investments ltd", "stoneridge limited",
            "riziki julia enterprises k limited", "afri fields investment ltd", "abbigoh enterprises limited",
            "simplex africa limited", "nelken solutions kenya limited", "dondan holdings limited",
            "urim and thummim enterprises", "mariana suppliers", "egalaxy kenya limited",
            "yvette supplies and agencies", "the herbive pest services", "nawada enterprises",
            "jojakika general supplies", "kelyn enterprises", "kenruche holdings limited",
            "nasirax enterprises", "besiobei engineering services", "twi twi company limited",
            "putmek services limited", "winterfell general construction limited", "jovinm contractors and suppliers co.ltd",
            "black africa security services", "suter brands", "afro group limited",
            "taitex construction company limited", "masters international limited", "sylva enterprises", "Sachira General Suppliers",
            "INTRINSIC ELECTRICAL COMPANY", "Emakale enterprises", "KEYHOLDER ENTERPRISES", "qaizen (e.a) limited",
            "DEYMO CONSTRUCTION AND CONSULTANCY COMPANY LIMITED", "GITARAMA ENTERPRISES", "green village east africa",
            "WAIKWAMBU ENTERPRISES", "SOLEX LINK ELECTRICAL", "IDENTITEE SUPPLY (E.A)", "nyamci enterprise",
            "LOURO ENTERPRISES", "SWIFT OPTION AGENCIES", "BISAMZ TECHNOLOGY LIMITED", "BE-FIFTEEN INVESTMENTS COMPANY LIMITED ",
            "e-net publishers and designs ltd", "galanticha enterprises limited", "ardha jila general supplies limited",
            "TOFEI CONSTRUCTION COMPANY LIMITED", "gutole traders limited",
        ]


        status = ConfigBusinessProfileStatus.objects.get(pk=1)
        business_profile = BusinessProfile.objects.create(
            name=random.choice(BUSINESSES),
            identity_type_id=6,
            identity_number="CPR/0%s/%s" % (random.randint(10, 99), random.randint(10000, 99999)),
            location_coodinates="%s,%s" % (random.uniform(-1.35, -1.5), random.uniform(36, 37)),
            physical_address="%s, %s road, %s, %s, %s" % (
                random.randint(5, 99),
                random.choice(["Popo", "South C", "Madaraka", "Lang'ata", "Rongai", "Mombasa"]),
                random.choice(["Nairobi South"]),
                "Nairobi", "Kenya"
            ),
            created_by_id=3,
            last_status=status,
            last_status_date=timezone.now()
        )
        business_profile_status = BusinessProfileStatus.objects.create(
            business_profile=business_profile,
            approved_by_id=3,
            created_by_id=3,
            status=status
        )
        loan_profile = LoanProfile.objects.create(
            credit_limit=random.choice((50000, 400000, 1500000, 75000)),
            business_profile=business_profile,
            created_by_id=3,
            profile_type_id=2
        )

        return loan_profile

    def create_individual_loan_profile(profile_type=1):
        #get names
        gender = random.choice(GENDERS)
        full_names = names.get_full_name(gender)

        #create profiles
        individual_profile = IndividualProfile.objects.create(
            first_name=full_names.split(" ")[0],
            last_name=full_names.split(" ")[1],
            profile_type=profile_type,
            mobile_phone_number=("+2547%s%s%s" % (
                random.choice([0,1,2,3]),
                random.choice(range(9)),
                random.randint(100000, 999999),
            )),
            email=("%s@%s.com" % (
                (
                    "%s.%s" % tuple(full_names.lower().split(' ')),
                    random.choice(EMAIL_PROVIDERS)
                )
            )),
            identity_number="%s" % (random.randint(20000000, 39999999)),
            identity_type_id=random.choice([2, 3, 4, 5, 7, 8]),
            gender=GENDERS.index(gender),
            created_by_id=3
        )
        loan_profile = LoanProfile.objects.create(
            individual_profile=individual_profile,
            credit_limit=random.choice((5000, 40000, 1500)),
            created_by_id=3,
            profile_type_id=1
        )

        return loan_profile

    with db_transaction.atomic():
        for client_type in ("individual", "group", "business"):
            for i in range(random.randint(60, 100)):
                if client_type == "individual":
                    loan_profile = create_individual_loan_profile()
                elif client_type == "group":
                    the_loan_profile = create_group_loan_profile()

                    for u in range(random.randint(3, 5)):
                        role = random.choice((1, 2, 3))
                        profile_type = random.choice([
                            "individual", "individual", 
                            "individual", "individual", 
                            "business", "group"
                        ])

                        group_role = ConfigLoanGroupRole.objects.get(pk=random.choice([1,2,3,4,4,4,4,4,4,4,4,4,4,4]))
                        group_member = GroupMembership.objects.create(
                            loan_group_profile=the_loan_profile.group_profile,
                            group_role=group_role,
                            created_by_id=3
                        )

                        if profile_type == "individual":
                            loan_profile = create_individual_loan_profile(profile_type=2)
                            group_member.member_individual = loan_profile.individual_profile
                        elif profile_type == "business":
                            loan_profile = create_business_loan_profile()
                            group_member.member_business = loan_profile.business_profile
                        elif profile_type == "group":
                            loan_profile = create_group_loan_profile()
                            group_member.member_group = loan_profile.group_profile

                        group_member.save()

                elif client_type == "business":
                    the_loan_profile = create_business_loan_profile()

                    for c in range(random.randint(2, 10)):
                        role = ConfigBusinessRole.objects.get(pk=random.choice([1, 2, 3, 4, 5, 7, 7, 7, 7, 7, 7]))

                        profile_type = random.choice((
                            "individual", "individual", 
                            "individual", "individual", 
                            "business", "group"
                        ))
                        business_stakeholder = BusinessStakeholder.objects.create(
                            role=role,
                            business_profile=the_loan_profile.business_profile,
                            stake_percentage=random.choice([10, 5, 2.5, 15, 10, 34, 53, 26, 55, 50, 90, 65]),
                            created_by_id=3
                        )

                        if profile_type == "individual":
                            loan_profile = create_individual_loan_profile(profile_type=3)
                            business_stakeholder.stakeholding_individual = loan_profile.individual_profile
                        elif profile_type == "business":
                            loan_profile = create_business_loan_profile()
                            business_stakeholder.stakeholding_business = loan_profile.business_profile
                        elif profile_type == "group":
                            loan_profile = create_group_loan_profile()
                            business_stakeholder.stakeholding_group = loan_profile.group_profile

                        business_stakeholder.save()

def populate_product_accounts():
    loan_products = LoanProduct.objects.all()
    loan_profiles = LoanProfile.objects.all()

    with db_transaction.atomic():
        for loan_profile in loan_profiles:
            for loan_product in loan_products:
                level = random.choice(["origination", "servicing", "collections"])
                if level == "origination":
                    status_id = random.choice([11, 10, 9, 8, 7])
                elif level == "servicing":
                    status_id = random.choice([
                        1, 1, 1, 1, 1, 1, 1, 
                        1, 1, 1, 1, 1, 1, 1, 
                        6, 6, 6, 6, 6, 6, 
                        6, 6, 6, 6, 6, 6, 
                        6, 6, 6, 6, 6, 6, 
                        6, 6, 6, 6, 6, 6, 
                        2, 2, 2, 2, 2, 
                        2, 2, 2, 2, 2, 
                        2, 2, 2, 2, 2, 
                        3, 5, 6, 13, 12,
                        3, 5, 6, 13, 12
                    ])
                elif level == "collections":
                    status_id = random.choice([4, 14])

                account = LoanAccount.objects.create(
                    product=loan_product,
                    repayment_model_id=1,
                    loan_profile=loan_profile,
                    account_number=utils.get_reference_no(17),
                    notes="No notes...",
                    created_by_id=3,
                    current_account_status_id=status_id,
                    current_account_status_date=timezone.now()
                )
                
                status = LoanAccountStatus.objects.create(
                    account=account,
                    status_id=status_id,
                    reason="Reason X",
                    approved_by_id=3,
                    created_by_id=3,
                )

                if account.repayment_model.code == "TRM_001":
                    loan_term = LoanTerm.objects.create(
                        loan_account=account,
                        loan_amount=random.uniform(
                            float(loan_product.min_amount),
                            float(loan_product.max_amount)
                        ),
                        loan_amount_currency_id=1,
                        loan_amount_disbursal_date=None,
                        repayment_period=loan_product.default_repayment_period,
                        repayment_period_unit=loan_product.default_repayment_period_unit,
                        repayment_frequency=loan_product.default_repayment_frequency,
                        grace_period=loan_product.default_repayment_grace_period,
                        grace_period_unit=loan_product.default_repayment_grace_period_unit,
                        interest_rate=loan_product.default_interest_rate,
                        created_by_id=3
                    )
                elif account.repayment_model.code == "TRM_002":
                    #for overdraft/revolving facilities
                    pass

                if status_id == 3:
                    loan_term2 = LoanTerm.objects.create(
                        loan_account=account,
                        loan_amount=random.uniform(
                            float(loan_product.min_amount),
                            float(loan_product.max_amount)
                        ),
                        loan_amount_currency_id=1,
                        loan_amount_disbursal_date=None,
                        repayment_period=(loan_product.default_repayment_period or 0) + 6,
                        repayment_period_unit=loan_product.default_repayment_period_unit,
                        repayment_frequency=loan_product.default_repayment_frequency,
                        grace_period=(loan_product.default_repayment_grace_period or 0) * 2,
                        grace_period_unit=loan_product.default_repayment_grace_period_unit,
                        interest_rate=(loan_product.default_interest_rate or 0) * D("0.85"),
                        created_by_id=3
                    )   

                    loan_term.terms_restructured = loan_term2
                    loan_term.terms_restructured_date = timezone.now()

                    loan_term.save()
                elif status_id in (2, 6, 5):
                    account.risk_classification_id = 1
                    account.save()
                elif status_id == 1:
                    account.risk_classification_id = 4
                    account.save()
                elif status_id == (12, 13):
                    account.risk_classification_id = 6
                    account.save()
                elif status_id == 14:
                    account.risk_classification_id = random.choice((4, 3, 2, 5, 5, 5))
                    account.save()


def setup_transactions():
    pass

if __name__ == "__main__":
    populate_profiles()
