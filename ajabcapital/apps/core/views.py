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
from . import (utils as core_utils, forms as core_forms)

@login_required
def dashboard(request):
    user = request.user

    context = {}
    
    return TemplateResponse(request, "core/dashboard.html", context)

@login_required
def main_menu(request):
    return TemplateResponse(request, "core/main_menu.html", {

    })

@login_required
def notifications(request):
    return TemplateResponse(request, "core/notifications.html", {

    })
