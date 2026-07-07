from celery import shared_task
from django.core.mail import send_mail


@shared_task
def wyslij_mailing_task(temat, tresc, odbiorcy):
    send_mail(
        subject=temat,
        message=tresc,
        from_email=None,
        recipient_list=odbiorcy,
        fail_silently=False,
    )

    return len(odbiorcy)


@shared_task
def test_celery_task():
    return "Celery działa poprawnie"
