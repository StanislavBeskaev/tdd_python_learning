from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def send_login_email(request: HttpRequest) -> HttpResponse:
    """Отправка сообщения для входа в систему"""
    email = request.POST["email"]
    send_mail(
        subject="Your login link for Superlists",
        message="body text tbc",
        from_email="noreply@superlists",
        recipient_list=[email]
    )
    return redirect("/")
