from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import CustomUser


@shared_task
def new_signup(id):
    user = CustomUser.objects.get(pk=id)
    subject = "Welcome to corecare"
    body = render_to_string("emails/signup_success.html", {"user": user})
    mail = EmailMessage(
        subject=subject, body=body, from_email="saiyedafzal0@gmail.com", to=[user.email]
    )
    mail.content_subtype = "html"
    mail.mixed_subtype = "related"
    mail.send()
