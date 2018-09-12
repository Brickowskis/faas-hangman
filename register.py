import logging, boto3

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):

    logger.info('Handling event {} - context {}', event, context)

    player_name = event['data']['command']['arguments'][0]
    phone_number = event['data']['twilio']['From']

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    player_table = dynamodb.Table('HangmanPlayer')

    player_table.put_item(
        Item={
            'phoneNumber': phone_number,
            'playerState': 'REGISTERED',
            'playerName': player_name
        }
    )

    return build_response("Successfully registered")


def build_response(body):
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Sms>{body}</Sms></Response>'
