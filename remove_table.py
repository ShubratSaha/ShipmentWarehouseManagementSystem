import boto3

client = boto3.client('dynamodb', region_name='ap-south-1')

try:
    resp = client.delete_table(
        TableName="Shipments",
    )
    print("Table deleted successfully!")
except Exception as e:
    print("Error deleting table:")
    print(e)
