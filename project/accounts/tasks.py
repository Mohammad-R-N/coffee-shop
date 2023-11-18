from celery import shared_task
from accounts.models import Otp
from datetime import datetime, timedelta
import pytz
from django.core.mail import send_mail
from config import settings


@shared_task
def remove_expired_otp_codes():
    expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=2)
    Otp.objects.filter(created__lt=expired_time).delete()


@shared_task
def send_email(email, code):
    send_mail(
        "OTP CODE",
        f"{code}",
        f"{settings.EMAIL_HOST_USER}",
        [f"{email}"],
        fail_silently=True,
    )
