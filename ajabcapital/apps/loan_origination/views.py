from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.http import (
    Http404, JsonResponse, HttpResponseForbidden
)

from django.shortcuts import resolve_url, render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST, require_GET

import json
import random
import logging

from . import forms, facades
from . import (utils as origination_utils, forms as core_forms)

from ..loan import facades as loan_facades

def start(request, product_pk=None):
    context = dict()

    if request.method == "POST":
        form = forms.PrequalificationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            full_name = data.get('full_name')
            age = data.get('age')
            gender = data.get('gender')
            location = data.get('location')
            loan_amount_range = data.get('loan_amount_range')
            credit_score_range = data.get('credit_score_range')
            revenue_range = data.get('revenue_range')
            loan_purpose = data.get('loan_purpose')

            is_prequalified = False

            if credit_score_range in ("CSR_004", "CSR_005", "CSR_006", "CSR_007"):
                is_prequalified = True

            if loan_amount_range > revenue_range:
                is_prequalified = False

            context['is_prequalified'] = is_prequalified
            context['data'] = data
        else:
            context['form'] = form

    return TemplateResponse(request, "origination/start.html", context)

def apply_product(request, product_pk):
    context = {}
    template_name = "origination/identity_verification.html"

    if request.method == "POST":
        context['verified'] = True

        n = 0
        while n:
            n += 1

            if n == 10000000000000000000000000:
                n = 0

        template_name = "origination/identity_verification_done.html"

    return TemplateResponse(request, template_name, context)


def loan_terms(request):
    context = {}
    
    template_name = "origination/loan_terms.html"

    if request.method == "POST":
        n = 0
        while n:
            n += 1

            if n == 10000000000000000000000000:
                n = 0
                
        template_name = "origination/loan_processing.html"

    return TemplateResponse(request, template_name, context)

def loan_processing(request):
    context = {}
    template_name = "origination/loan_processing.html"
    return TemplateResponse(request, template_name, context)    