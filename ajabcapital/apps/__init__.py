'''
The idea is that, the application is divisible in 
functionality in a way that its pluggable for both 
Saccos and Microfinance institutions.

1. core
    - core_accounts
        models:
        o - account
        o - product_accounts
    - core_users
        functionality:
        f - dashboard
        f - audit trail
        f - password reset
        f - update profile
        f - roles and capabilities
        f - default user to have all capabilities
        f - activate/deactivate user (N/I)
        models:
        o - user
        o - password_tokens
        o - log trail
        o - capability
        o - role_capability

2. utility modules:
    - core_sms
        functionality:
        f - create and poll sms objects for sending
        f - send polled sms objects via selected sms interfaces
        f - receive sms requests and push them to the crm
        f - 
        models:
        o - sms_in
        o - sms_out
        o - sms_schedule
        views:
        v - an interface to send sms,
        v - an interface to view incoming/outgoing texts
        v - an interface to add sms schedules
        v - an interface to add sms templates [To be added in version 2]
    - core_ussd
        functionality:
        f - create a ussd request
        f - store ussd sessions to make it easier to return to where you left off
        f - cache sessions for speed purposes [on client commission only]
        f - ussd analytics
        models:
        o - ussd_request
        o - ussd_request_body_base
        views:
        v - dashboard
        v - ussd request lists (indicate where the customer fell off, or whether they were locked out)
        v - opening 

3. backoffice:
    - backoffice_crm
        functionality:
        f - create customer profiles
        f - link system to customer.
        f - create campaigns [other campaigns will be added to the system via other modules]
        f - create schedules for campaigns
        f - provide a dashboard to show interaction, top customers and their equivalent performance
        models:
        o - customer_profile
        o - documents
        o - identity
    - backoffice_credit_decisioning
        functionality:
        f - provide a form to define the business logic, among filterable items include:[
            ACCOUNT:
            - has paid for deposit protection fund
            - has transacted for more than 6 months
            KYC:
            - has identity: identity exists in providers db; metropol, creditinfo
            - has identity matching with mpesa transaction; deposit protection fund.
            RISK:
            - choose between providers: Metropol, CreditInfo...
            - choose range for credit score
            - choose range for ppi 
            - choose financial malpractices
            - choose income...
        ]
        f - loan limit rules: [
            this is open to interpretation by paying client...
            loan limit is defined in the loan module
        ]

    - backoffice_loans
    functionality
        - setup mobile loan names and other business requirements
        - define fees for penalties, interest
        - setup disbusement and repayment accounts
        - 

4. payments
    - payments_mpesa

5. loans
    - loan_limit
    - loan_disbursements
    - loan_repayments
    - loan_collection
    - loan_origination
        = loan_origination_ussd
        = loan_origination_web

##-----------------to be added later-------------------
6. risk_management
    - risk_management_metropol
    - risk_management_credit_info
    - risk_management_transunion
    - credit_decisioning_partners

#------------------------------------------------------

7. analytics
8. credit_officer
9. loan_origination/syndicated_loan_origination
10. loan_origination/loan_origination_android
11. loan_origination/loan_origination_telegram
12. financial_accounting
10. loans/loan_recovery
11. backoffice/backoffice_compliance_mfi
12. core/core_emails
    models: 
        o - email_template
        o - email_template_sent
    - core_pdf N/I
    - core_charts N/I
13. backoffice_kyc (N/I)
14. core_partners
        models:
            o - partner
            o - partner_users
'''