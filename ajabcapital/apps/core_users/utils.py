from . import models

def is_capable(user, path):
    if user is not None:
        if user.is_superuser:
            return True
        elif user.role:
            role = user.role

            role_capabilities = models.RoleCapability.objects.all()

            if role == models.SUPER_ADMIN:
                return True
            elif role == models.AJAB_CAPITAL_STAFF:
                role_capabilities = role_capabilities.filter(
                    role_code=role,
                    capability__path=path,
                    capability__role_category=models.AJAB_CAPITAL_USER
                )
                return role_capabilities.exists()
            elif role == models.LOAN_PARTNER_ADMINISTRATOR:
                role_capabilities = role_capabilities.filter(
                    role_code=role,
                    capability__path=path,
                    capability__role_category=models.LOAN_PARTNER_USER
                )
                return role_capabilities.exists()
            elif role == models.LOAN_PARTNER_OFFICER:
                role_capabilities = role_capabilities.filter(
                    role_code=role,
                    capability__path=path,
                    capability__role_category=models.LOAN_PARTNER_USER
                )
                return role_capabilities.exists()

            elif role == models.LOAN_CLIENT:
                role_capabilities = role_capabilities.filter(
                    role_code=role,
                    capability__path=path,
                    capability__role_category=models.LOAN_CLIENT_USER
                )
                return role_capabilities.exists()

    return False