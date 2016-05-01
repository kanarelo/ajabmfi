from ajabcapital.apps.core.models import *

from .accounting import *
from .accounts import *
from .config import *
from .products import *
from .transactions import *

@login_required
def dashboard(request):
    context = dict(
        total_principal_due=D('12236723'),
        total_dues=D('23080728'),
        avg_days_in_arrears=D('6.4'),
        max_days_in_arrears=D('129'),
        portfolio_by_status=[
            {'name': 'Perfoming & Outstanding', 'value': D("370512702"), 'color': "#010303"},
            {'name': 'Perfoming', 'value': D("602043257"), 'color': "#0c4246"},
            {'name': 'Non-Performing', 'value': D("124007572"), 'color': "#147179"},
            {'name': 'Reperforming', 'value': D("30922057"), 'color': "#22c0cd"},
            {'name': 'Write-Off', 'value': D("19000257"), 'color': "#b4f2f7"}
        ],
        portfolio_by_fund=[
            {'name': 'Owner\'s Equity', 'value': D("430278500"), 'color': "#1F3A52"},
            {'name': 'Youth Fund Grant', 'value': D("267107322"), 'color': "#41A186"},
            {'name': 'Strathmore SBS Grant', 'value': D("380432322"), 'color': "#7EBF5D"},
            {'name': 'Rockafellar Grant', 'value': D("107557000"), 'color': "#D3F689"}
        ],
        portfolio_by_repayment_model=[
            {'name': 'Term', 'value': D("906700572"), 'color': "#600d1e"},
            {'name': 'Revolving', 'value': D("103808900"), 'color': "#C5183B"},
            {'name': 'Bullet', 'value': D("55400000"), 'color': "#ff6d8a"},
        ],
    )
    return TemplateResponse(request, "loan/dashboard.html", context)

@login_required
def loan_accounts(request):
    accounts = LoanAccount.objects.active().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(accounts, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "loan/loan_accounts.html", {
        'accounts': accounts
    })

@login_required
def loan_funds(request):
    funds = LoanFund.objects.all().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(funds, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        funds = paginator.page(page)
    except PageNotAnInteger:
        funds = paginator.page(1)
    except EmptyPage:
        funds = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "loan/loan_funds.html", {
        'funds': funds
    })

@login_required
def loan_products(request):
    products = LoanProduct.objects.active().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "loan/loan_products.html", {
        "products": products
    })

@login_required
def loan_accounting(request):
    return TemplateResponse(request, "loan/loan_accounting.html", {
    })

@login_required
def loan_reports(request):
    return TemplateResponse(request, "loan/loan_reports.html", {
    })
