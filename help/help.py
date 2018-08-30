import logging

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"


def lambda_handler(event, context):
    to_number = event['To']
    from_number = event['From']
    body = event['Body']

    logging.info("Received help request from %s", from_number)

    return build_response(f'Actions:{CRLB}register{CRLB}status')


def build_response(body):
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Sms>{body}</Sms></Response>'