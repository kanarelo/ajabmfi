from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.http import (
    Http404, JsonResponse, HttpResponseForbidden
)

from django.shortcuts import resolve_url, render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST, require_GET

import json
import random
import logging

from datetime import datetime

from . import forms

from ..core import (
    utils as core_utils,
    forms as core_forms
)
from ..loan import (
    facades as loan_facades
)
from .models import *

@login_required
def dashboard(request):
    context = {}

    context.update(
        applications_by_product=[
            {'name': 'M-Loan', 'value': D('41293209.22'), 'color': '#010303'},
            {'name': 'SME Mobile Loan', 'value': D('21233629.22'), 'color': '#0c4246'},
            {'name': 'Jipange Simple Mortgage', 'value': D('101293629.22'), 'color': '#147179'},
            {'name': 'Motor Cycle Loan', 'value': D('9093629.22'), 'color': '#22c0cd'},
        ],
        individual_borrowers=862,
        group_borrowers=276,
        sme_borrowers=78,
        total_borrowers=(862 + 276 + 78),
        sms_sent=237,
        sms_left=122,
        emails_sent=92,
        sms_received=141,
    )

    return TemplateResponse(request, "crm/dashboard.html", context)

def search_client(request):
    return TemplateResponse(request, "crm/search_client.html", {})  

@login_required
def individuals(request):
    profiles = IndividualProfile.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(profiles, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "crm/individual_profiles.html", {
        "profiles": profiles
    })

@login_required
def businesses(request):
    profiles = BusinessProfile.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(profiles, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "crm/business_profiles.html", {
        "profiles": profiles
    })

@login_required
def groups(request):
    profiles = GroupProfile.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(profiles, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "crm/group_profiles.html", {
        "profiles": profiles
    })

@login_required
def messages(request):
    messages = Message.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(messages, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "crm/messages.html", {
        "messages": messages
    })

@login_required
def campaigns(request):
    campaigns = Campaign.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(campaigns, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        campaigns = paginator.page(page)
    except PageNotAnInteger:
        campaigns = paginator.page(1)
    except EmptyPage:
        campaigns = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "crm/campaigns.html", {
        "campaigns": campaigns
    })

@login_required
def templates(request):
    templates = MessageTemplate.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(templates, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        templates = paginator.page(page)
    except PageNotAnInteger:
        templates = paginator.page(1)
    except EmptyPage:
        templates = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "crm/templates.html", {
        "templates": templates
    })

@login_required
def applications(request):
    applications = [
        dict(
            applicant_name='Onesmus Mukewa Wekalao',
            identity_type='Passport Number',
            identity_number='A1938021',
            loan_purpose='Business Expansion',
            crb_score='700',
            amount=D('290000'),
            color="rgba(255,33,43,0.1)",
            status='Accepted',
            created_at=datetime.now()
        ),
        dict(
            applicant_name='Synacor LTD',
            identity_type='Business Registration Number',
            identity_number='CPR/001/20014',
            loan_purpose='Business Expansion',
            crb_score='700',
            amount=D('290000'),
            color="rgba(255,33,43,0.1)",
            status='Accepted',
            created_at=datetime.now()
        ),
        dict(
            applicant_name='Justus Matanda',
            identity_type='National ID',
            identity_number='22883390',
            loan_purpose='Asset Finance',
            crb_score='410',
            amount=D('430000'),
            status='Rejected',
            color="rgba(255,33,43,0.1)",
            created_at=datetime.now()
        ), 
        dict(
            applicant_name='Mary Nafula',
            identity_type='National ID',
            identity_number='32090023',
            loan_purpose='Asset Finance',
            crb_score='740',
            amount=D('1900000'),
            status='Accepted',
            created_at=datetime.now()
        ), 
    ]
    return TemplateResponse(request, "crm/applications.html", {
        'applications': applications
    })