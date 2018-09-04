import logging, uuid, datetime, boto3, json
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('Handling event {} - context {}', event, context)

    responseMessage = event["data"]["response"]["sms"]
    errors = event["data"]["errors"]

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
        responseMessage = responseMessage + "\n" + "A game record exists"
    else:
        logger.warning('No existing game record to stop')
        responseMessage = responseMessage + "\n" + "A game record does not exist"

    # If the game state is "created", update the game state to "running"
    if game["gameState"] == "created":
        # set state to over
        game["gameState"] = 'running'

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
            errors = e
            responseMessage = responseMessage + "\n" + "Error ["+e+"]"
            print("Unexpected error: %s" % e)

    if gameExists and game["gameState"] == "running":
        responseMessage = responseMessage + "\n" + "Game started"
        responseMessage = responseMessage + "\n" + "Id ["+game["Id"]+"]"
        responseMessage = responseMessage + "\n" + "Start Datetime ["+game["startDatetime"]+"]"
        responseMessage = responseMessage + "\n" + "Game State ["+game["gameState"]+"]"
        responseMessage = responseMessage + "\n" + "Solution ["+game["solution"]+"]"

    event["data"]["errors"] = errors
    event["data"]["game"] = game
    event["data"]["response"]["sms"] = responseMessage

    return event
