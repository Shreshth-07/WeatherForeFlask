from twilio.rest import Client
import os

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4fe368a469148898aa84b19777bf80af'
auth_token = 'd3328ebef84245191400bfd9d868eb9c'

client = Client(account_sid, auth_token)

from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+5491122521185'

def send_WA(body_):
    message = client.messages.create(
                              body=body_,
                              from_=from_whatsapp_number,
                              to=to_whatsapp_number
                          )

