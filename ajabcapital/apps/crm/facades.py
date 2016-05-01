from .models import *

SMS = "MT_001"
EMAIL = "MT_002"
NOTIFICATION = "MT_003"
INTERNAL = "MT_004"
ALL_MEDIA = "MT_005"

MESSAGE_PENDING_DELIVERY = "MS_001"
MESSAGE_DELIVERED = "MS_002"
MESSAGE_FAILED = "MS_003"
MESSAGE_CANCELLED = "MS_004"

def create_message(
    message_type_code=None, 
    message_template_code=None, 
    individual_profile=None,
    business_profile=None,
    group_profile=None,
    message=None,
    status_code=None,
    template_arguments=None
):
    if message_type in (SMS, EMAIL, ALL_MEDIA):
        message_type = ConfigMessageType.objects.get(code=message_type_code)


    if template_arguments is None:
        template_arguments = {}

    if status_code is None:
        status_code = MESSAGE_PENDING_DELIVERY

    status = ConfigMessageStatus.objects.get(code=status_code)

    if message is None:
        if message_template_code:
            template = MessageTemplate.objects.get(code=message_template_code)
            message  = template.template.format(template_arguments)

    if (individual_profile or business_profile or group_profile):
        return 

    the_message = Message.objects.create(
        individual_profile=individual_profile,
        business_profile=business_profile,
        group_profile=group_profile,
        message_type=message_type,
        template=template,
        message=message,
        status=status,
    )

    return the_message