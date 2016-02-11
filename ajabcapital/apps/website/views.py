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

from . import forms

from ..core import (
    utils as core_utils,
    forms as core_forms
)

def index(request):
    return TemplateResponse(request, "website/index.html", {})

def about_us(request):
    return TemplateResponse(request, "website/about_us.html", {})

def careers(request):
    return TemplateResponse(request, "website/careers.html", {})

def partners(request):
    return TemplateResponse(request, "website/partners.html", {})

def demo_bookings(request):
    if request.method == "POST":
        form = forms.DemoBookingForm(request.POST)

        if form.is_valid():
            booking = form.save()

            messages.add_message(
                request, messages.INFO, (
                    "You have booked a demo. Our sales representatives "
                    "will get in touch soon."
                )
            )
            return redirect("/")
    else:
        form = forms.DemoBookingForm()
            
    return TemplateResponse(request, "website/demo_booking.html", {
        'form': form
    })