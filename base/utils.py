from django.core.mail import send_mail
from django.conf import settings


def send_registration_email(user, raw_password):
    """
    Sends a registration email with login credentials.

    :param user: CustomUser instance (Registered User)
    :param raw_password: Generated password for the user
    """
    subject = "Welcome to Medivault - Registration Successful"
    message = f"""
    Hello {user.first_name},

    Your registration was successful! You can log in with the following credentials:

    🔹 **Login Email:** {user.email}  
    🔹 **Login Password:** {raw_password}  

    You must log in first and reset your password.

    ➡️ [Click here to log in](http://localhost:8000)

    Please keep your credentials secure.

    Regards,  
    **Medivault Team**
    """

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
