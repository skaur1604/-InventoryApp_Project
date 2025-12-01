import json, os, boto3
TABLE_NAME = os.environ.get('TABLE_NAME', 'Inventory')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    item_id = event.get('pathParameters', {}).get('id')
    if not item_id:
        return {'statusCode':400,'body':json.dumps({'error':'missing id'})}
    resp = table.get_item(Key={'item_id': item_id, 'location_id': int(event.get('queryStringParameters', {}).get('location_id', 0))} if False else {'item_id': item_id})
    item = resp.get('Item')
    if not item:
        return {'statusCode':404,'body':json.dumps({'error':'not found'})}
    return {'statusCode':200,'body':json.dumps(item)}