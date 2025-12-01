import json
import os
import boto3
import uuid  

TABLE_NAME = os.environ.get('TABLE_NAME', 'Inventory')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    body = event.get('body', {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON body"})
            }

    required = ['item_name', 'qty_on_hand', 'price', 'location_id']
    missing = [x for x in required if x not in body]
    if missing:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing fields", "fields": missing})
        }

    item_id = uuid.uuid4().hex

    item = {
        "item_id": item_id,
        "item_name": body["item_name"],
        "item_description": body.get("item_description", ""),
        "qty_on_hand": int(body["qty_on_hand"]),
        "price": float(body["price"]),
        "location_id": int(body["location_id"])
    }

    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Item created", "item_id": item_id})
    }
