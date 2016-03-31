from .accounting import *
from .accounts import *
from .config import *
from .products import *
from .transactions import *

@login_required
def dashboard(request):
	return TemplateResponse(request, "loan/dashboard.html", {
	})

@login_required
def loan_accounts(request):
	return TemplateResponse(request, "loan/loan_accounts.html", {
	})

@login_required
def loan_funds(request):
	return TemplateResponse(request, "loan/loan_funds.html", {
	})

@login_required
def loan_transactions(request):
	return TemplateResponse(request, "loan/loan_transactions.html", {
	})

@login_required
def loan_products(request):
	return TemplateResponse(request, "loan/loan_products.html", {
	})

@login_required
def loan_accounting(request):
	return TemplateResponse(request, "loan/loan_accounting.html", {
	})

@login_required
def loan_reports(request):
	return TemplateResponse(request, "loan/loan_reports.html", {
	})
