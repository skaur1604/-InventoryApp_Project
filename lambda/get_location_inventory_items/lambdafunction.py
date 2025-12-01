import json, os, boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ.get('TABLE_NAME', 'Inventory')
GSI_NAME = os.environ.get('GSI_NAME', 'LocationIndex')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    location_id = event.get('pathParameters', {}).get('id')
    if location_id is None:
        return {'statusCode':400,'body':json.dumps({'error':'missing location id'})}
    resp = table.query(IndexName=GSI_NAME, KeyConditionExpression=Key('location_id').eq(int(location_id)))
    items = resp.get('Items', [])
    return {'statusCode':200,'body':json.dumps(items)}