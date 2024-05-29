from django.core.mail import send_mail
from typing import Dict


def send_order_info_mail(data: Dict[str, str], email: str):
    """
    Функция отправки почтовых сообщений с информацией о заказе
    """
    recipient_email = email
    subject = 'Payment Information'
    message = f"Номер заказа: {data['orderId']}" \
              f"\nСылка на оплату заказа {data['url']}"
    sender_email = 'django.shop@mail.ru'

    send_mail(subject, message, sender_email, [recipient_email])
