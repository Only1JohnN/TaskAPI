from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta


def send_verification_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    token_expiry_time = timezone.now() + timedelta(hours=1)
    
    user.verification_token_expiry = token_expiry_time
    user.save()
    
    verification_link = f"{settings.SITE_DOMAIN}/verify-email/?uid={uid}&token={token}"

    send_mail(
        subject='Verify your email',
        message=f'Click the link to verify: {verification_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

