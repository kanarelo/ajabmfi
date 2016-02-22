from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.http import (Http404, JsonResponse, HttpResponseForbidden, HttpResponse)

from django.utils import timezone
from django.utils.text import slugify

from django.shortcuts import resolve_url, render, get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.views.decorators.http import require_POST, require_GET

import json
import random

import datetime
import calendar

from ..forms import *

from decimal import Decimal as D

@login_required
def create_product(request):
    context = {}

    if request.method == "POST":
        form = CreateProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            product = LoanProduct.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                is_active=data.get('is_active'),
                loan_type=data.get('loan_type'),
                default_repayment_period=data.get('default_repayment_period'),
                default_repayment_period_unit=data.get('default_repayment_period_unit'),
                default_repayment_frequency=data.get('default_repayment_frequency'),
                repayment_grace_period_type=data.get('repayment_grace_period_type'),
                default_repayment_grace_period=data.get('default_repayment_grace_period'),
                default_repayment_grace_period_unit=data.get('default_repayment_grace_period_unit'),
                amount_currency=data.get('amount_currency'),
                default_amount=data.get('default_amount'),
                min_amount=data.get('min_amount'),
                max_amount=data.get('max_amount'),
                interest_calculation_method=data.get('interest_calculation_method'),
                default_interest_rate=data.get('default_interest_rate'),
                min_interest_rate=data.get('min_interest_rate'),
                max_interest_rate=data.get('max_interest_rate'),
                created_by=request.user
            )
            
            return redirect("/")

    elif request.method == "GET":
        form = CreateProductForm()

    context.update(form=form)

    return TemplateResponse(request, "loan/products/create.html", context)

@login_required
def edit_product(request):
    context = {}

    if request.method == "POST":
        pass
    elif request.method == "GET":
        pass

    return TemplateResponse(request, "loan/products/edit.html", context)
