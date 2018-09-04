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
        # generate the first and only game id. Starting a new game will reuse this uuid
        print("Game does not exist!")
        game["Id"] = str(uuid.uuid4())
        logger.info('No existing game record. Creating game id {}', game["Id"])
        responseMessage = responseMessage + "\n" + "A game record does not exist"

    # If the game state is "over", update the game state to "created"
    if game["gameState"] == "over":
        # generate timestamp
        game["startDatetime"] = str(datetime.datetime.utcnow().isoformat())

        # set state to created
        game["gameState"] = 'created'

        # set solution to the command
        game["solution"] = event["data"]["command"]["arguments"][1]

        try:
            # upsert the game - DynamoDB call
            response = hangmanGame.update_item(
                Key={
                    'Id': game["Id"]
                },
                UpdateExpression='SET startDatetime = :std, gameState = :st, solution = :sln',
                ExpressionAttributeValues={
                    ':std': game["startDatetime"],
                    ':st': game["gameState"],
                    ':sln': game["solution"],
                }
            )
        except ClientError as e:
            errors = e
            responseMessage = responseMessage + "\n" + "Error ["+e+"]"
            print("Unexpected error: %s" % e)

    if game["gameState"] == "created":
        responseMessage = responseMessage + "\n" + "Game created"
        responseMessage = responseMessage + "\n" + "Id ["+game["Id"]+"]"
        responseMessage = responseMessage + "\n" + "Start Datetime ["+game["startDatetime"]+"]"
        responseMessage = responseMessage + "\n" + "Game State ["+game["gameState"]+"]"
        responseMessage = responseMessage + "\n" + "Solution ["+game["solution"]+"]"

    event["data"]["errors"] = errors
    event["data"]["game"] = game
    event["data"]["response"]["sms"] = responseMessage

    return event
