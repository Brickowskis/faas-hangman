import logging, boto3, nexmo

def handler(event, context):
    ssm = boto3.client('ssm')
    logging.info(f'Handling event {event} - context {context}')

    errors = event['data']['errors']
    responseMessage = event['data']['response']['sms']

    response = ssm.get_parameters(
        Names=[
            '/nexmo/key',
            '/nexmo/secret',
        ],
        WithDecryption=False
    )

    nexmo_auth = {
        'key': response['Parameters'][0]['Value'],
        'secret': response['Parameters'][1]['Value']
    }

    client = nexmo.Client(
        key = nexmo_auth['key'],
        secret = nexmo_auth['secret']
    )

    response = client.send_message(
        {'from': event['data']['sms']['To'],
         'to': event['data']['sms']['From'],
         'text': responseMessage}
    )
    response = response['messages'][0]
    status = response['status']

    if status == '0':
        message = response['message-id']
        logging.info(f'Sent Nexmo message : status {status} - message id {message}')

    else:
        errorText = response['error-text']
        logging.error(f'Error sending Nexmo message : status {status} - error {errorText}')

    return event
