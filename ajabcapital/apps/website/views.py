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

from . import forms

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
			data = form.cleaned_data

	else:
		form = forms.DemoBookingForm()
			
	return TemplateResponse(request, "website/demo_booking.html", {
		'form': form
	})