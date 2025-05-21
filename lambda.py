import json
import boto3
import random
import os
import logging
from boto3.dynamodb.conditions import Key

# Set up structured logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use environment variable for table name (better for reusability and security)
TABLE_NAME = os.getenv('QUOTE_TABLE_NAME', 'quotegeneratortable')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def get_random_quote(greeting_name):
    //"""Query DynamoDB and return a random quote for the given greeting_name."""
    response = table.query(
        KeyConditionExpression=Key('greeting_name').eq(greeting_name)
    )
    items = response.get('Items', [])
    if items:
        return random.choice(items).get('quote', 'No quote available.')
    else:
        return None

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    greeting_name = event.get('queryStringParameters', {}).get('greeting_name', 'Guest')

    if not isinstance(greeting_name, str) or not greeting_name.strip():
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid greeting_name'}),
            'headers': {'Content-Type': 'application/json'}
        }

    try:
        quote = get_random_quote(greeting_name)
        if quote:
            body = {'quote': quote}
            status_code = 200
        else:
            body = {'message': f'No quotes found for greeting: {greeting_name}'}
            status_code = 404

    except Exception as e:
        logger.error("Error fetching quote: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error fetching quote: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }

    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }

  
