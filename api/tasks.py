from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# @shared_task
# def send_contact_or_partners_mail(type, data, _from, _to):
#     if type == "contact":
#         mail_subject = "CoreCare Contact Us"
#         mail_message = f"""A Contact Message from
#         Name: {data['first_name']} {data['last_name']}
#         email : {data['email']}
#         message: {data['message']}"""
#     elif type == "partner":
#         mail_subject = "CoreCare Partner Request"
#         mail_message = f"""
#         Name: {data['name']}
#         Number: {data['number']}
#         email : {data['email']}
#         detail: {data['detail']}"""
#     send_mail(mail_subject, mail_message,_from,_to)

@shared_task
def send_contact_or_partners_mail(type, data, _from, _to):
    if type == "contact":
        mail_subject = "Corecare contact us"
        _from_name = f"{data['first_name']} {data['last_name']}"
        number = data.get('number', "Not Available")
        message = data['message']
    else:
        _from_name = data['name']
        mail_subject = "Corecare Partner Request"
        number = data['number']
        message = data['detail']
    mail_context = {
        'request_type': type, 
        'from': _from_name, 
        'number': number, 
        "email": data['email'],
        "message": message
        }
    mail_body = render_to_string('emails/contact_and_partners.html', context=mail_context)
    mail_obj = EmailMessage(mail_subject, mail_body, _from, _to)
    mail_obj.content_subtype = "html"
    mail_obj.mixed_subtype = "related"
    mail_obj.send()
