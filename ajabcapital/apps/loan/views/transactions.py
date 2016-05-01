from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.db.models import Sum, Avg, Max, Q, Count
from django.db import transaction as db_transaction

from django.shortcuts import resolve_url
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.http import (
	HttpResponseRedirect, 
	HttpResponseForbidden, 
	JsonResponse, 
	HttpResponse,
	Http404
)

from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST, require_GET

from ajabcapital.apps.core.models import *

@login_required
def loan_transactions(request):
    transactions = LedgerTransaction.objects.loan_transactions(
    ).order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(transactions, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)


    return TemplateResponse(request, "loan/loan_transactions.html", {
        'transactions': transactions
    })
