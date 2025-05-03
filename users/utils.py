from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from urllib.parse import quote

def generate_uid_and_token(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_verification_email(user):
    """
    Sends the email verification link after registration.
    """
    user.save()
    uid, token = generate_uid_and_token(user)  # Get the UID and token using our function
    
    # Set token expiry time
    token_expiry_time = timezone.now() + timedelta(hours=1)
    user.verification_token_expiry = token_expiry_time
    user.save()

    verification_link = f"{settings.SITE_DOMAIN}/verify-email/?uid={quote(uid)}&token={quote(token)}"

    # Render the email content
    html_message = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_link': verification_link,
        'current_year': timezone.now().year,
    })

    send_mail(
        subject='Verify your Email Address',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,     # For Production, set to True
        html_message=html_message,
    )

def send_password_reset_email(user):
    """Send password reset email with verification link."""
    user.save()
    uid, token = generate_uid_and_token(user)
    
    # Set expiry for token (1 hour from now)
    token_expiry_time = timezone.now() + timedelta(hours=1)
    user.verification_token_expiry = token_expiry_time

    reset_link = f"{settings.SITE_DOMAIN}/reset-password/?uid={uid}&token={token}"

    html_message = render_to_string('emails/password_reset.html', {
        'user': user,
        'reset_link': reset_link,
        'current_year': timezone.now().year,
    })

    send_mail(
        subject='Password Reset Request',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,     # For Production, set to True
        html_message=html_message,
    )

    

def send_welcome_email(user):
    login_link = f"{settings.SITE_DOMAIN}/login/"

    html_message = render_to_string('emails/verify_email.html', {
        'user': user,
        'login_link': login_link,
        'current_year': timezone.now().year,
    })

    send_mail(
        subject='Welcome to TaskAPI!',
        message=f'Click the link to login your account: {login_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,     # For Production, set to True
        html_message=html_message,
    )
    
    
def send_password_change_confirmation_email(user):
    """Send confirmation email after password has been reset by the user."""
    html_message = render_to_string('emails/password_change_confirmation.html', {
        'user': user,
        'current_year': timezone.now().year,
    })

    send_mail(
        subject='Your Password Has Been Changed',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,     # For Production, set to True
        html_message=html_message,
    )