import logging, boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

def handler(event, context):
    logging.info(f'Handling event {event} - context {context}')

    responseMessage = event["data"]["response"]["sms"]
    errors = event["data"]["errors"]

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

    if len(runningGames) == 1:
        try:
            game = runningGames[0]
            stop_game(game, gameTable)
            responseMessage = append_message(responseMessage, 'Game stopped', game)
        except ClientError as e:
            errors = e
            responseMessage = append_message(responseMessage, f'Error [{e}]')

    elif len(createdGames) == 1:
        game = createdGames[0]
        responseMessage = append_message(responseMessage, 'A game is created but not running', game)

    else:
        game = {}
        responseMessage = append_message(responseMessage, 'No games exist to stop')

    event['data']['errors'] = errors
    event['data']['game'] = game
    event['data']['response']['sms'] = responseMessage

    return event


def stop_game(game, gameTable):
    game['gameState'] = 'over'
    # upsert the game - DynamoDB call
    response = gameTable.update_item(
        Key={
            'Id': game['Id']
        },
        UpdateExpression='SET gameState = :st',
        ExpressionAttributeValues={
            ':st': game['gameState']
        }
    )


def append_message(response, message, game = None):
    if game is None:
        return f"{response}\n{message}"
    else:
        return f"{response}\n{message}" + \
               f"\nId [{game['Id']}]" + \
               f"\nStart Datetime [{game['startDatetime']}]" + \
               f"\nGame State [{game['gameState']}]" + \
               f"\nSolution [{game['solution']}]"