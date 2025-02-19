import json
import boto3
import random
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('quotegeneratortable')

    # Parse query string params safely
    greeting_name = event.get('queryStringParameters', {}).get('greeting_name', 'Guest')

    try:
        # Query DynamoDB table
        response = table.query(
            KeyConditionExpression=Key('greeting_name').eq(greeting_name)
        )
        items = response.get('Items', [])

        # Check if items exist and select a random quote
        if items:
            selection = random.choice(items)  # Direct selection
            quote = selection.get('quote', 'No quote available.')
        else:
            quote = "No quotes found for this greeting."

    except Exception as e:
        quote = f"Error fetching quote: {str(e)}"

    # Construct HTTP response object
    response_object = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"quote":quote})
    }

    return response_object


  
