from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_contact_or_partners_mail(type, data, _from, _to):
    if type == "contact":
        mail_subject = "CoreCare Contact Us"
        mail_message = f"""A Contact Message from
        Name: {data['first_name']} {data['last_name']}
        email : {data['email']}
        message: {data['message']}"""
    elif type == "partner":
        mail_subject = "CoreCare Partner Request"
        mail_message = f"""
        Name: {data['name']}
        Number: {data['number']}
        email : {data['email']}
        detail: {data['detail']}"""
    send_mail(mail_subject, mail_message,_from,_to)
