import logging, uuid, datetime, boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

def handler(event, context):
    logging.info(f'Handling event {event} - context {context}')

    responseMessage = event['data']['response']['sms']
    solution = event['data']['command']['arguments'][1]
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
        try:
            game = create_game(solution, gameTable)
            responseMessage = append_message(responseMessage, 'Game created')
        except ClientError as e:
            errors = e
            responseMessage = append_message(responseMessage, f'Error [{e}]')

    if len(runningGames) == 1:
        game = runningGames[0]
        responseMessage = append_message(responseMessage, 'A game is already running')

    if len(createdGames) == 1:
        game = createdGames[0]
        responseMessage = responseMessage + '\n' + 'A game is already created'


    responseMessage = (
        f"{responseMessage}" +
        f"\nId [{game['Id']}]" +
        f"\nStart Datetime [{game['startDatetime']}]" +
        f"\nGame State [{game['gameState']}]" +
        f"\nSolution [{game['solution']}]"
    )

    event['data']['errors'] = errors
    event['data']['game'] = game
    event['data']['response']['sms'] = responseMessage

    return event


def create_game(solution, gameTable):
    game = {
        'Id': str(uuid.uuid4()),
        # generate timestamp
        'startDatetime': str(datetime.datetime.utcnow().isoformat()),
        # set state to created
        'gameState': 'created',
        # set solution to the command
        'solution': solution
    }

    # upsert the game - DynamoDB call
    response = gameTable.update_item(
        Key={
            'Id': game['Id']
        },
        UpdateExpression='SET startDatetime = :std, gameState = :st, solution = :sln',
        ExpressionAttributeValues={
            ':std': game['startDatetime'],
            ':st': game['gameState'],
            ':sln': game['solution'],
        }
    )
    return game


def append_message(response, message):
    return f"{response}\n{message}"