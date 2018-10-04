import logging
import boto3
import json
from boto3.dynamodb.conditions import Attr

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('Handling event {} - context {}', event, context)
    phone_number = event['data']['twilio']['From']

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    player_table = dynamodb.Table('HangmanPlayer')
    game_table = dynamodb.Table('HangmanGame')

    response = game_table.scan(
        FilterExpression=Attr('gameState').ne('over')
    )
    running_games = list()
    for game in response['Items']:
        if game['gameState'] == 'running':
            running_games.append(game)

    game = running_games[0]
    response = player_table.get_item(
        Key={
            'phoneNumber': phone_number,
            'gameId': game['Id']
        }
    )
    player_info = response['Item']
    print(player_info)

    guesses = json.loads(player_info['guesses'])
    lives_remaining = 6 - len(guesses['wrong'])

    print(lives_remaining)

    current_solve_state = game['solution']
    unguessed_letters = (set(list(current_solve_state)) - set(list(guesses['correct'])))
    for letter in unguessed_letters:
        current_solve_state = current_solve_state.replace(letter, "*")

    print(current_solve_state)

    return build_response(f'{CRLB}{CRLB}'+letter_available())


def build_response(body):
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Sms>{body}</Sms></Response>'

def letter_available():
    return f'A B C D E F G H I J L M N{CRLB}O P Q R S T U V W X Y Z'
