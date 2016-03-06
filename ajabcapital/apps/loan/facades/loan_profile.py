from django.db.models import Q, Sum, F
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ajabcapital.apps.core.facades import *
from .loan_transactions import *

def send_notification_to_profile(loan_profile):
    pass