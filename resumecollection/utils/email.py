from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config.settings.local import EMAIL_HOST_USER

User = get_user_model()


def send_password_update_email(user, reset_password_link):
    subject = "Reset Password"
    message = f"Hello {user.name},\n\nReset Password Link: {reset_password_link}"
    send_mail(subject, message, EMAIL_HOST_USER, [user.email])
