from celery import shared_task
from django.template.loader import render_to_string
from .models import Order
from api.models import Service
from django.db.models import Case, When
from django.core.mail import EmailMessage

@shared_task
def order_success_mail(order_id, recommanded_ids):
    order = Order.objects.select_related('user').get(receipt=order_id)
    preserve_ids = Case(*[When(id=id, then=index) for index, id in enumerate(recommanded_ids)])
    services = Service.objects.filter(id__in=recommanded_ids).order_by(preserve_ids)
    subject = f"Order {order_id}"
    body = render_to_string('emails/order_success.html', {'order': order, "services": services})
    mail = EmailMessage(subject=subject, body=body, from_email="saiyedafzal0@gmail.com", to=[order.user.email])
    mail.content_subtype = "html"
    mail.mixed_subtype = "related"
    mail.send()
