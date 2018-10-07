import logging, boto3

from boto3.dynamodb.conditions import Attr

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"

def handler(event, context):
    logging.info(f'Handling event {event} - context {context}')

    player_name = event['data']['command']['arguments'][0]
    phone_number = event['data']['twilio']['From']

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    game_table = dynamodb.Table('HangmanGame')
    player_table = dynamodb.Table('HangmanPlayer')

    # Get the running game
    response = game_table.scan(
        FilterExpression=Attr('gameState').ne('over')
    )
    running_games = list()
    for game in response['Items']:
        if game['gameState'] == 'running':
            running_games.append(game)

    # Register the player for the running game
    game = running_games[0]
    player_table.put_item(
        Item={
            'phoneNumber': phone_number,
            'gameId': game['Id'],
            'playerState': 'REGISTERED',
            'playerName': player_name
        }
    )

    return build_response("Successfully registered")


def build_response(body):
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Sms>{body}</Sms></Response>'
