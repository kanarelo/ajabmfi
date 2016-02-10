from .. import models as auth_models

def role_exists(**kwargs):
    return True
    # return Role.objects.filter(**kwargs).exists()
