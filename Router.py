import logging, boto3

def handler(event, context):
    logging.info(f'Handling event {event} - context {context}')

    to_number = event['data']['sms']['To']
    from_number = event['data']['sms']['From']
    body = event['data']['sms']['Body']

    logging.info(f'Messaged directed to {to_number} from {from_number} with body {body}')

    action = body.split()[0].strip().lower()
    logging.info(f'Found action {action}')

    if action == 'game':
        event['data']['command']['type'] = 'admin'
        event['data']['command']['operation'] = 'game'
        event['data']['command']['arguments'] = body.split()[1:]
        if not isAdminNumber(from_number):
            event['data']['errors'] = 'You do not have permission to execute this command.'
            event['data']['response']['sms'] = 'You do not have permission to execute this command.'
    elif action == 'register':
        event['data']['command']['type'] = 'player'
        event['data']['command']['operation'] = 'register'
        event['data']['command']['arguments'] = body.split()[1:]
    elif action == 'status':
        event['data']['command']['type'] = 'player'
        event['data']['command']['operation'] = 'status'
        event['data']['command']['arguments'] = body.split()[1:]
    else:
        event['data']['command']['type'] = 'player'
        event['data']['command']['operation'] = 'guess'
        event['data']['command']['arguments'] = action

    return event


def isAdminNumber(from_number):
    ssm = boto3.client('ssm')

    response = ssm.get_parameters(
        Names=[
            '/admin/phoneNumbers'
        ],
        WithDecryption=False
    )
    numberStr = response['Parameters'][0]['Value']
    adminNumbers = [number.strip() for number in numberStr.split(',')]
    return from_number in adminNumbers
