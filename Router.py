import logging


def lambda_handler(event, context):
    to_number = event['data']['twilio']['To']
    from_number = event['data']['twilio']['From']
    body = event['data']['twilio']['Body']

    errors = event["data"]["errors"]

    logging.info(f'Messaged directed to {to_number} from {from_number} with body {body}')

    action = body.split()[0].strip().lower()
    logging.info(f'Found action {action}')

    if action in ['game']:
        event['data']['command']['type'] = 'admin'
        event['data']['command']['operation'] = 'game'
        event['data']['command']['arguments'] = body.split()[1:]
        if not isAdminNumber(from_number):
            errors = f'{from_number} does not have access to execute admin commands.'
            event['data']['response']['sms'] = 'You do not have permission to execute this command.'
    elif action == 'register':
        event['data']['command']['type'] = 'player'
        event['data']['command']['operation'] = 'register'
        event['data']['command']['arguments'] = body.split()[1:]

    event['data']['errors'] = errors
    return event


def isAdminNumber(from_number):
    #                       Trevor          Tim             John
    return from_number in ['+13025109165', '+16104056406', '+16103577793']
