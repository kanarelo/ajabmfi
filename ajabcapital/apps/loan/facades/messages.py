from ...crm.facades import *

SMS = "MT_001"
EMAIL = "MT_002"
NOTIFICATION = "MT_003"
INTERNAL = "MT_004"
ALL_MEDIA = "MT_005"

MESSAGE_PENDING_DELIVERY = "MS_001"
MESSAGE_DELIVERED = "MS_002"
MESSAGE_FAILED = "MS_003"
MESSAGE_CANCELLED = "MS_004"

def send_notification_to_profile(
    loan_profile, 
    message, 
    message_type_code=NOTIFICATION,
    message_template_code=None,
    status_code=MESSAGE_DELIVERED,
    template_arguments=None
):
    return create_message(
        message=message,
        status_code=status_code,
        message_type_code=message_type_code, 
        template_arguments=template_arguments,
        message_template_code=message_template_code, 
        group_profile=loan_profile.group_profile,
        business_profile=loan_profile.business_profile,
        individual_profile=loan_profile.individual_profile
    )
