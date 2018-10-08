import logging
import boto3
from boto3.dynamodb.conditions import Attr

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"


def handler(event, context):
    logging.info(f'Handling event {event} - context {context}')

    player_name = event['data']['command']['arguments'][0]
    phone_number = event['data']['twilio']['From']
    errors = event["data"]["errors"]

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    game_table = dynamodb.Table('HangmanGame')
    player_table = dynamodb.Table('HangmanPlayer')

    # Get the running game
    response = game_table.scan(
        FilterExpression=Attr('gameState').eq('created')
    )
    created_games = list()
    for game in response['Items']:
        if game['gameState'] == 'created':
            created_games.append(game)

    if len(created_games) == 0:
        event['data']['response']['sms'] = f"Unfortunately, you can't register for the game at this time. " \
                                           f"The game has either not been created or is already running."
        return event

    # Register the player for the running game
    game = created_games[0]
    player_table.put_item(
        Item={
            'phoneNumber': phone_number,
            'gameId': game['Id'],
            'playerState': 'REGISTERED',
            'playerName': player_name,
            'guesses': '{ \"correct\": [], \"wrong\" : [] }'
        }
    )

    event['data']['errors'] = errors
    event['data']['game'] = game
    event['data']['response']['sms'] = f'{player_name} you are registered!'

    return event
