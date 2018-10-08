import datetime
import json
import logging

import boto3
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALLOWED_MISSES = 6


def handler(event, context):
    guess = event['data']['command']['arguments'][0]
    from_number = event['data']['twilio']['From']

    logging.info(f"Received guess {guess} from {from_number}")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    game_table = dynamodb.Table('HangmanGame')
    player_table = dynamodb.Table('HangmanPlayer')

    # Get created games from the game table - should be 0 or 1
    gameQuery = game_table.scan(
        FilterExpression=Attr('gameState').eq('running')
    )
    game = retrieve_game(gameQuery)

    # Get created games from the game table - should be 0 or 1
    gamePlayer = player_table.scan(
        FilterExpression=Attr('phoneNumber').eq(from_number) & Attr('gameId').eq(game['Id'])
    )
    player = retrieve_game(gamePlayer)

    if game is not None and player is not None and player_is_alive(player):
        process_guess(game, player, guess, player_table)

    return event


def retrieve_game(running_game):
    if len(running_game['Items']) == 0:
        return None
    else:
        return running_game['Items'][0]


def retrieve_player(game_player):
    if len(game_player['Items']) == 0:
        return None
    else:
        return game_player['Items'][0]


def player_is_alive(game_player):
    guesses = json.loads(game_player['guesses'])
    if len(guesses['wrong']) < ALLOWED_MISSES:
        return True
    return False


def process_guess(game, player, guess, player_table):
    solution = game['solution']
    guesses = json.loads(player['guesses'])
    correct_guesses = guesses['correct']
    wrong_guesses = guesses['wrong']
    if guess not in correct_guesses and guess not in wrong_guesses:
        if guess == solution:
            correct_guesses.append(guess)
            guesses['correct'] = correct_guesses
            update_guesses(player, json.dumps(guesses), player_table)
            mark_winner(player, player_table)
        elif len(guess) == 1 and guess in solution:
            correct_guesses.append(guess)
            guesses['correct'] = correct_guesses
            update_guesses(player, json.dumps(guesses), player_table)
            if is_winner(solution, correct_guesses):
                mark_winner(player, player_table)
        else:
            wrong_guesses.append(guess)
            guesses['wrong'] = wrong_guesses
            update_guesses(player, json.dumps(guesses), player_table)


def update_guesses(player, guesses, player_table):
    player_table.update_item(
        Key={
            'phoneNumber': player['phoneNumber'],
            'gameId': player['gameId']
        },
        UpdateExpression='SET guesses = :g, lastGuessDateTime = :dt',
        ExpressionAttributeValues={
            ':g': guesses,
            ':dt': str(datetime.datetime.utcnow().isoformat())
        }
    )


def mark_winner(player, player_table):
    player_table.update_item(
        Key={
            'phoneNumber': player['phoneNumber'],
            'gameId': player['gameId']
        },
        UpdateExpression='SET playerState = :ps',
        ExpressionAttributeValues={
            ':ps': 'WINNER'
        }
    )


def is_winner(solution, correct_guesses):
    return set(solution) == set(correct_guesses)
