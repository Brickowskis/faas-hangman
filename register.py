import logging, boto3

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"


def handler(event, context):
    #to_number = event['To']
    #from_number = event['From']
    #logging.info(f'Received registration request for {from_number}')

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    playerTable = dynamodb.Table('HangmanPlayer')

    playerTable.put_item(
        Item={
            'phoneNumber': '6105551234'
        }
    )

    return build_response("Successfully registered")


def build_response(body):
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Sms>{body}</Sms></Response>'
