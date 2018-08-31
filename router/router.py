import logging


def register():
    return "register"


def status():
    return "status"


def default():
    return "help"


routes = {
    "default": default(),
    "register": register(),
    "status": status()
}


def lambda_handler(event, context):
    to_number = event['To']
    from_number = event['From']
    body = event['Body']

    logging.info('Messaged directed to {to_number} from {from_number} with body {body}')

    action = body.split()[0].strip().lower()
    logging.info('Found action {action}')
    event['route'] = routes.get(action, default())
    return event
