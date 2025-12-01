import json, os, boto3
TABLE_NAME = os.environ.get('TABLE_NAME','Inventory')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    item_id = event.get('pathParameters', {}).get('id')
    if not item_id:
        return {'statusCode':400,'body':json.dumps({'error':'missing id'})}
    table.delete_item(Key={'item_id': item_id})
    return {'statusCode':200,'body':json.dumps({'message':'deleted','item_id':item_id})}