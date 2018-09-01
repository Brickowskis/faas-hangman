import logging, uuid, datetime, boto3, json
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('Handling event {} - context {}', event, context)

    # Initial game state
    game = {
        "gameState": "over"
    }

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    hangmanGame = dynamodb.Table('HangmanGame')

    # Get the game from the game table
    response = hangmanGame.scan()
    gameExists = len(response["Items"]) == 1
    if gameExists:
        game = response["Items"][0]
        logger.info('Found existing game record {}', game)
    else:
        logger.warning('No existing game record to stop')

    # If the game state is "over", update the game state to "created"
    if game["gameState"] != "over":
        # set state to over
        game["gameState"] = 'over'

        try:
            # upsert the game - DynamoDB call
            response = hangmanGame.update_item(
                Key={
                    'Id': game["Id"]
                },
                UpdateExpression='SET gameState = :st',
                ExpressionAttributeValues={
                    ':st': game["gameState"]
                }
            )
        except ClientError as e:
            print("Unexpected error: %s" % e)

    event["data"]["game"] = game

    return event
