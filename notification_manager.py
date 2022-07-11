from twilio.rest import Client
import smtplib

TWILIO_VIRTUAL_NUMBER = "+19127156145"
TWILIO_VERIFIED_NUMBER = "+972509701013"

TWILIO_SID = 'AC3acb01867887d8cc6984ac7e373d3074'
TWILIO_AUTH_TOKEN = '016b8500710dfde50fcb9f20ce1b6c7c'

MY_EMAIL = "joangelaphyton@gmail.com"
MY_PASSWORD = "3uxZ6S$ELdEw("

EMAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )