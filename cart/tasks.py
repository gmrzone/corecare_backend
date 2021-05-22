from celery import shared_task
from django.template.loader import render_to_string
from .models import Order
from api.models import Service
from django.db.models import Case, When
from django.core.mail import EmailMessage
import weasyprint
from io import BytesIO
from django.conf import settings
import os
@shared_task
def order_success_mail(order_id, recommanded_ids):
    order = Order.objects.select_related('category', 'user', 'coupon').prefetch_related('items', 'items__service', 'coupon__category').get(receipt=order_id)
    preserve_ids = Case(*[When(id=id, then=index) for index, id in enumerate(recommanded_ids)])
    recommanded_services = Service.objects.filter(id__in=recommanded_ids).order_by(preserve_ids)
    subject = f"Order {order_id}"
    body = render_to_string('emails/order_success.html', {'order': order, "services": recommanded_services})
    mail = EmailMessage(subject=subject, body=body, from_email="saiyedafzal0@gmail.com", to=[order.user.email])
    mail.content_subtype = "html"
    mail.mixed_subtype = "related"
    pdf_str = render_to_string('invoice/invoice.html', {"order": order})
    empty_obj = BytesIO()
    stylesheet = [weasyprint.CSS(settings.BASE_DIR / "staticfiles/static/css/main.css")]
    weasyprint.HTML(string=pdf_str).write_pdf(target=empty_obj, stylesheets=stylesheet)
    mail.attach(f"{order_id}.pdf", empty_obj.getvalue(), 'application/pdf')
    mail.send()
