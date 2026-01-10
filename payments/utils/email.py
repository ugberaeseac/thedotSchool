from django.core.mail import send_mail
from django.conf import settings
import resend



def send_success_email_with_resend(payment, discord):
    resend.api_key = settings.RESEND_API_KEY
    subject = 'Payment Successful - Welcome to The dotSchool'
    html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Payment Successful</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f5f7fb; padding: 20px;">
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0"
                            style="background: #ffffff; padding: 30px; border-radius: 8px;">
                            
                            <tr>
                                <td align="center" style="padding-bottom: 20px;">
                    <img 
                    src="https://res.cloudinary.com/dfngbmsno/image/upload/v1768043289/dotschool_logo_nthdib.png" 
                            alt="The dotSchool Logo" 
                            style="max-width:120px; width:100%; height:auto;"
                        >
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <h2 style="color: #2b3035;">Payment Successful</h2>

                                    <p>Hello <strong>{payment.full_name}</strong>,</p>

                                    <p>
                                        Congratulations! Your payment for the course
                                        <strong>{payment.course}</strong> has been successfully processed.
                                    </p>

                                    <p>
                                        You are now officially enrolled.
                                        Click the button below to join your class on Discord:
                                    </p>

                                    <p style="text-align: center; margin: 30px 0;">
                                        <a href="{discord}"
                                        style="
                                                background-color: #2b3035;
                                                color: #ffffff;
                                                padding: 14px 24px;
                                                text-decoration: none;
                                                border-radius: 6px;
                                                font-weight: 600;
                                        "
                                        target="_blank">
                                            Join the Class
                                        </a>
                                    </p>

                                    <p>
                                        Further announcements and instructions will be shared inside the class.
                                    </p>

                                    <p style="margin-top: 40px;">
                                        — <br>
                                        <strong>The dotSchool Team</strong>
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html> 
    """

    params: resend.Emails.SendParams = {
    "from": settings.RESEND_FROM_EMAIL,
    "to": [payment.email],
    "subject": subject,
    "html": html_message,
    }

    email = resend.Emails.send(params)
    print(email)




def send_success_email(payment, discord):
    subject = 'Payment Successful - Welcome to The dotSchool'
    text_message= f"""
    Hello {payment.full_name},

    Your payment for {payment.course} was successful.

    Join your class on Discord:
    {discord}

    — The dotSchool Team
    """
    html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Payment Successful</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f5f7fb; padding: 20px;">
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0"
                            style="background: #ffffff; padding: 30px; border-radius: 8px;">
                            
                            <tr>
                                <td align="center" style="padding-bottom: 20px;">
                    <img 
                    src="https://res.cloudinary.com/dfngbmsno/image/upload/v1768043289/dotschool_logo_nthdib.png" 
                            alt="The dotSchool Logo" 
                            style="max-width:120px; width:100%; height:auto;"
                        >
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <h2 style="color: #2b3035;">Payment Successful</h2>

                                    <p>Hello <strong>{payment.full_name}</strong>,</p>

                                    <p>
                                        Congratulations! Your payment for the course
                                        <strong>{payment.course}</strong> has been successfully processed.
                                    </p>

                                    <p>
                                        You are now officially enrolled.
                                        Click the button below to join your class on Discord:
                                    </p>

                                    <p style="text-align: center; margin: 30px 0;">
                                        <a href="{discord}"
                                        style="
                                                background-color: #2b3035;
                                                color: #ffffff;
                                                padding: 14px 24px;
                                                text-decoration: none;
                                                border-radius: 6px;
                                                font-weight: 600;
                                        "
                                        target="_blank">
                                            Join the Class
                                        </a>
                                    </p>

                                    <p>
                                        Further announcements and instructions will be shared inside the class.
                                    </p>

                                    <p style="margin-top: 40px;">
                                        — <br>
                                        <strong>The dotSchool Team</strong>
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html> 
    """
    
    send_mail(
        subject=subject,
        message=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[payment.email],
        html_message=html_message,
        fail_silently=False
    )