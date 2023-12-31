import logging

from accounts.models import Token
from django.contrib import auth, messages
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


def send_login_email(request: HttpRequest) -> HttpResponse:
    """Отправка сообщения для входа в систему"""
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login") + "?token=" + str(token.uid))
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        subject="Your login link for Superlists",
        message=message_body,
        from_email="noreply@superlists",
        recipient_list=[email],
    )
    logger.info(f"send login email for {email}")

    messages.success(request, "Check your email, you'll find a message with a link that will log you into the site.")
    return redirect("/")


def login(request: HttpRequest) -> HttpResponse:
    """Регистрация в системе"""
    user = auth.authenticate(uid=request.GET.get("token"))
    if user:
        auth.login(request, user)
        logger.info(f"login user {user.email}")
    return redirect("/")


def logout(request: HttpRequest) -> HttpResponse:
    """Выход из системы"""
    auth_logout(request)
    return redirect("/")
