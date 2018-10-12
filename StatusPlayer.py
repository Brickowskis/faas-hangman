import logging
import boto3
import json
from boto3.dynamodb.conditions import Attr

# https://support.twilio.com/hc/en-us/articles/223181468-How-do-I-Add-a-Line-Break-in-my-SMS-or-MMS-Message-
CRLB = "%0a"


def handler(event, context):
    logging.info(f'Handling event {event} - context {context}')

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

    if len(running_games) == 0:
        response_message = append_message("", 'There is no running game.')
        event['data']['response']['sms'] = response_message
        return event

    game = running_games[0]
    phone_number = event['data']['twilio']['From']
    response = player_table.get_item(
        Key={
            'phoneNumber': phone_number,
            'gameId': game['Id']
        }
    )

    if response.get("Item") is None:
        response_message = append_message("", 'Player was not found')
        event['data']['response']['sms'] = response_message
        return event

    player_info = response['Item']
    guesses = json.loads(player_info['guesses'])
    lives_remaining = 6 - len(guesses['wrong'])

    #Get the current solution state
    current_solve_state = game['solution']
    unguessed_letters = (set(list(current_solve_state)) - set(list(guesses['correct'])))
    for letter in unguessed_letters:
        current_solve_state = current_solve_state.replace(letter, "_")

    # Build the response message
    response_message = event['data']['response']['sms']

    if player_info['playerState'] == 'WINNER':
        response_message = f"{response_message} WINNER!"
        current_solve_state = game['solution']

    if player_info['playerState'] == 'DEAD':
        response_message = f"{response_message} + Sorry, you are now dead!"

    current_solve_state = " ".join(current_solve_state.upper())
    response_message = (
        f"{response_message}" +
        f"\nLives:    { lives_remaining }" +
        f"\nWord:     { current_solve_state } " +
        f"\nMisses:   { guesses['wrong'] }"
    )

    event['data']['game'] = game
    event['data']['response']['sms'] = response_message

    return event


def append_message(response, message):
    return f"{response}\n{message}"
