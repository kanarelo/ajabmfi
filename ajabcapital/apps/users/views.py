from django.contrib.auth import (
    REDIRECT_FIELD_NAME, 
    get_user_model, login as auth_login, 
    logout as auth_logout, 
    update_session_auth_hash,
    authenticate
)
from django.contrib.auth import (login as auth_login, authenticate)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, resolve

from django.db.models import Sum, Avg, Max, Q, Count
from django.db import transaction as db_transaction

from django.http import (
    Http404, JsonResponse, HttpResponseForbidden, 
    HttpResponse, HttpResponseRedirect
)
from django.shortcuts import resolve_url, render, get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.utils import timezone
from django.utils.text import slugify
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST, require_GET

import simplejson as json
import random
import datetime
import calendar

from decimal import Decimal as D

from ..core import (
    utils as core_utils
)
from . import (
    api as auth_api,
    forms as auth_forms,
    utils as auth_utils, 
    models as user_models
)

import logging

def dashboard(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.dashboard'):
        return HttpResponseForbidden('Access Denied')

#-------------------- activate/deactivate
@login_required
@require_POST
def activate_user(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.activate'):
        return HttpResponseForbidden('Access Denied')

    user_id = core_utils.get_int_or_None(request.objects.get('user_id'))

    #get the user to activate
    user = get_object_or_404(user_models.User, id=user_id)

    with db_transaction.atomic():
        logger.debug("action='users.activate' request_user_id=%s user_id=%s" % (request.user, user_id))
        auth_api.activate_user(user)

        core_utils.leave_user_message(
            request, "INFO", "You have successfully activated user %s" % user.get_full_name()
        )

    #where to redirect to after save
    redirect_to = request.POST.get('redirect_to', 'users:dashboard')
    return redirect(redirect_to)

@login_required
@require_POST
def deactivate_user(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.deactivate'):
        return HttpResponseForbidden('Access Denied')

    #get the user to activate
    user_id = core_utils.get_int_or_None(request.objects.get('user_id'))
    user = get_object_or_404(user_models.User, id=user_id)

    with db_transaction.atomic():
        logger.debug("action='users.activate' request_user_id=%s user_id=%s" % (request.user, user_id))
        auth_api.deactivate_user(user)

        core_utils.leave_user_message(
            request, "INFO", "You have successfully deactivated user %s" % user.get_full_name()
        )

    #where to redirect to after save
    redirect_to = request.POST.get('redirect_to', 'users:dashboard')
    return redirect(redirect_to)

#--------------------
@login_required
@require_POST
def add_user(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.add'):
        return HttpResponseForbidden('Access Denied')

    form = auth_forms.AddPartnerUserForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

        with db_transaction.atomic():
            user = auth_api.create_user(data)
            logger.debug(
                "action='users.add.partner' request_user_id=%s user_id=%s" % (
                    request.user, user.id
                )
            )

            redirect_to = request.POST.get('redirect_to', 'users:dashboard')
            return redirect(redirect_to)

#---------------------
@login_required
@require_GET
def view_profile(request):
    logger = logging.getLogger(__name__)
    user   = request.user

    user_id = core_utils.get_int_or_None(request.objects.get('user_id'))

    if not auth_utils.is_capable(user, 'users.add') or (user.id == user_id):
        return HttpResponseForbidden('Access Denied')

    context = {}

    return TemplateResponse(request, "users/view_profile.html", context)

@login_required
@require_POST
def edit_profile(request):
    user = request.user
    context = {}
    
    form = auth_forms.AddPartnerUserForm(data=request.POST, user=user)
    if form.is_valid():
        data = form.cleaned_data

        with db_transaction.atomic():
            user = auth_api.update_user(user, data)

            context['message'] = "Profile successfully updated."
            context['user'] = um_facades.get_user_dict(user)
    else:
        context['message'] = form.errors
        context['successful'] = False

    return JsonResponse(context)

#-------------------------
@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(
    request,
    template_name='auth/change_password.html',
    post_change_redirect=None,
    password_change_form=ChangeUserPasswordForm,
    extra_context=None
):

    context = {}

    if extra_context is not None:
        context.update(extra_context)

    if request.method == "POST":
        try:
            try:
                user_id = int(request.REQUEST.get('user_id'))
            except TypeError:
                user_id = request.user.id

            if request.user.id == user_id:
                user = request.user
            else:
                user = get_object_or_404(User, id=user_id)
        except ValueError as e:
            raise Http404('Must provide user id')

        if request.REQUEST.get('random-password') == "on":
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            context['successful'] = True
            # um_facades.send_password_been_reset_email(new_password)
        else:
            if user == request.user:
                form = ChangeUserPasswordForm(data=request.POST, user=user)
            else:
                if request.user.is_superuser and request.REQUEST.get('no-current'):
                    form = ChangePasswordForm(data=request.POST)
                else:
                    form = password_change_form(data=request.POST, user=user)

            if form.is_valid():
                data = form.cleaned_data

                new_password = data.get("new_password")
                user.set_password(new_password)

                # um_facades.send_password_been_reset_email(new_password)
                context['successful'] = True
            else:
                context['successful'] = False
                context['error'] = form.errors
                context['message'] = form.errors
        context['user'] = um_facades.get_user_dict(user)

        update_session_auth_hash(request, user)
                
        if request.is_ajax():
            return JsonResponse(context)
        else:
            return redirect('switchboard')
    else:
        if post_change_redirect is None:
            post_change_redirect = reverse('password_change_done')
        else:
            post_change_redirect = resolve_url(post_change_redirect)

        form = password_change_form(user=request.user)
        context.update(form=form, title=('Password change'))

        return TemplateResponse(request, template_name, context)

@require_POST
@login_required
@csrf_protect
@sensitive_post_parameters()
def send_reset_email(
    request,
    template_name='auth/password_reset_form.html',
    email_template_name='auth/password_reset_email.html',
    subject_template_name='auth/password_reset_subject.txt',
    password_reset_form=PasswordResetForm,
    token_generator=default_token_generator,
    post_reset_redirect=None,
    from_email=None,
    extra_context=None,
    html_email_template_name=None,
    extra_email_context=None
):
    form = password_reset_form(request.POST)
    if form.is_valid():
        opts = {
            'use_https': request.is_secure(),
            'token_generator': token_generator,
            'from_email': from_email,
            'email_template_name': email_template_name,
            'subject_template_name': subject_template_name,
            'request': request,
            'html_email_template_name': html_email_template_name,
            'domain_override': settings.BASE_URL
        }
        form.save(**opts)

        if post_reset_redirect is not None:
            return HttpResponseRedirect(post_reset_redirect)
        else: 
            return JsonResponse({
                'successful': True,
                'message': "Password reset password sent to '%s'" % form.cleaned_data['email']
            })
    else:
        return JsonResponse({
            'successful': False,
            'message': 'Something wrong with the email address'
        })

@csrf_protect
def password_reset(
    request,
    template_name='auth/password_reset_form.html',
    email_template_name='auth/password_reset_email.html',
    subject_template_name='auth/password_reset_subject.txt',
    password_reset_form=PasswordResetForm,
    token_generator=default_token_generator,
    post_reset_redirect=None,
    from_email=None,
    extra_context=None,
    html_email_template_name=None,
    extra_email_context=None
):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        return send_reset_email(
            request,
            template_name=template_name,
            email_template_name=email_template_name,
            subject_template_name=subject_template_name,
            password_reset_form=password_reset_form,
            token_generator=token_generator,
            post_reset_redirect=post_reset_redirect,
            from_email=from_email,
            extra_context=extra_context,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context,
        )
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': ('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

def password_reset_done(
    request,
    template_name='auth/password_reset_done.html',
    extra_context=None
):
    context = {
        'title': ('Password reset sent'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

@sensitive_post_parameters()
@never_cache
def password_reset_confirm(
    request, uidb64=None, token=None,
    template_name='auth/password_reset_confirm.html',
    token_generator=default_token_generator,
    set_password_form=SetPasswordForm,
    post_reset_redirect=None,
    extra_context=None
):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = ('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = ('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

def password_reset_complete(request,
                            template_name='auth/password_reset_complete.html',
                            extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': ('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)