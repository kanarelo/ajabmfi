from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.http import (
    Http404, JsonResponse, HttpResponseForbidden
)

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST, require_GET

import json
import random
import logging

def index(request):
    return TemplateResponse(request, "web/index.html", {})

def about_us(request):
    return TemplateResponse(request, "web/about_us.html", {})

def careers(request):
    return TemplateResponse(request, "web/careers.html", {})

def partners(request):
    return TemplateResponse(request, "web/partners.html", {})
