import logging
import json


def lambda_handler(event, context):
    logging.info('Path params: %s', event['pathParameters'])
    logging.info('Query string: %s', event['queryStringParameters'])
    logging.info('Request context: %s', event['requestContext'])
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(event)
    }
