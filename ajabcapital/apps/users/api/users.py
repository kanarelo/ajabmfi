from .. import (
    decorators,
    models as auth_models
)
from . import roles

@decorators.logtrail(action_path="users.add.partner")
def create_partner_user(data):
    user = auth_models.User.objects.create(
        fullname="%s %s %s" % (first_name, middle_name or '', surname),
        email=email,
        role=role
    )
    return user

#-------------------------------------data-----------------------------------
@decorators.logtrail(action_path="users.activate")
def activate_user(user):
    if user is not None and not user.is_activate:
        user.is_activate = True
        user.save()

    return user

@decorators.logtrail(action_path="users.deactivate")
def deactivate_user(user):
    if user is not None and user.is_activate:
        user.is_activate = False
        user.save()

    return user

