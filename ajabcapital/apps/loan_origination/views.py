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

@login_required
def dashboard(request):
    user = request.user

    context = {}
    
    return TemplateResponse(request, "origination/dashboard.html", context)

@login_required
def my_pipeline(request):
    
    return TemplateResponse(request, "origination/mypipeline.html", {

    })

@login_required
def reports(request):
    return TemplateResponse(request, "origination/reports.html", {

    })
