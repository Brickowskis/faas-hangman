import boto3
import logging
from boto3.dynamodb.conditions import Attr

def handler(event, context):
    logging.info('Handling event {event} - context {context}')

    responseMessage = event['data']['response']['sms']
    errors = event['data']['errors']

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    gameTable = dynamodb.Table('HangmanGame')

    # Get created games from the game table - should be 0 or 1
    response = gameTable.scan(
        FilterExpression=Attr('gameState').ne('over')
    )

    createdGames = list()
    runningGames = list()
    for game in response['Items']:
        if game['gameState'] == 'created':
            createdGames.append(game)
        if game['gameState'] == 'running':
            runningGames.append(game)

    if len(createdGames) == 0 and len(runningGames) == 0:
        game = {}
        responseMessage = append_message(responseMessage, 'There are no created or running games')

    elif len(runningGames) == 1:
        game = runningGames[0]
        responseMessage = append_message(responseMessage, 'Active running game:', game)

    elif len(createdGames) == 1:
        game = createdGames[0]
        responseMessage = append_message(responseMessage, 'Active created game:', game)

    event['data']['errors'] = errors
    event['data']['game'] = game
    event['data']['response']['sms'] = responseMessage

    return event


def append_message(response, message, game=None):
    if game is None:
        return f"{response}\n{message}"
    else:
        return f"{response}\n{message}" + \
               f"\nId [{game['Id']}]" + \
               f"\nStart Datetime [{game['startDatetime']}]" + \
               f"\nGame State [{game['gameState']}]" + \
               f"\nSolution [{game['solution']}]"

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
        logger.warning('No existing game record')
        responseMessage = responseMessage + "\n" + "A game record does not exist"

    if gameExists:
        responseMessage = responseMessage + "\n" + "Game status"
        responseMessage = responseMessage + "\n" + "Id [" + game["Id"] + "]"
        responseMessage = responseMessage + "\n" + "Start Datetime [" + game["startDatetime"] + "]"
        responseMessage = responseMessage + "\n" + "Game State [" + game["gameState"] + "]"
        responseMessage = responseMessage + "\n" + "Solution [" + game["solution"] + "]"

    event["data"]["errors"] = errors
    event["data"]["game"] = game
    event["data"]["response"]["sms"] = responseMessage

    return event
