import boto3
import os

def lambda_function(event: any, context: any):
    i = (event)
    user = ''
    if 'user' in event:
        user = event['user']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: No body in the event'),
            'value': i
        }
    visit_count = 0

    #Create dynamobd client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    #Get the current visit count
    # print(table.creation_date_time)
    response = table.get_item(Key={"User": user})
    if "Item" in response:
        visit_count = response["Item"]["count"]

    visit_count += 1

    table.put_item(Item={"User": user, "count" : visit_count})


    message = f"Hello {user}! You have visited the page {visit_count} times!"
    return{"message": message}


#Below code is not part of labmda functoin, just for testing.

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "VisitorTable"
    event = {"user": "something"}
    print(lambda_function(event, None))