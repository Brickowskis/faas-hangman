import logging, uuid, datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info('Handling event {} - context {}', event, context)

    # Get the game from the game table - DynamoDB call
    game = {
       "state": "over"
    }

    # If the game state is 'over', update the game state to 'created'
    if game['state'] == "over":
        # generate game id
        game['id'] = uuid.uuid4()

        # generate timestamp
        game['startDatetime'] = datetime.datetime.utcnow().isoformat()

        # set state to created
        game['state'] = 'created'

        # set solution to the command
        game['solution'] = event['data']['command']['arguments'][1]

        # update the game - DynamoDB call
        event['data']['game'] = game

    return event

