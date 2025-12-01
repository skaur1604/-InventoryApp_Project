import json, os, boto3
from decimal import Decimal

TABLE_NAME = os.environ.get('TABLE_NAME', 'Inventory')
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    return obj