import logging, boto3
from twilio.rest import Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    ssm = boto3.client('ssm')
    logger.info('Handling event {} - context {}', event, context)

    errors = event['data']['errors']
    responseMessage = event['data']['response']['sms']

    response = ssm.get_parameters(
        Names=[
            '/twilio/account_sid',
            '/twilio/auth_token',
        ],
        WithDecryption=False
    )

    twilio_auth = {
        'account-sid': response['Parameters'][0]['Value'],
        'auth-token': response['Parameters'][1]['Value']
    }

    client = Client(
        twilio_auth['account-sid'],
        twilio_auth['auth-token']
    )

    message = client.messages.create(
        body  = responseMessage,
        from_ = event['data']['twilio']['To'],
        to    = event['data']['twilio']['From']
    )

    if (message.error_code != None):
        logger.error('Error sending Twilio  message : code{} - message {}', message.error_code, message.error_message)

    return event
