import requests
import json
import boto3
import requests
import datetime

def get_rest_api_id(client):
    api_list = client.get_rest_apis()
    for api in api_list['items']:
        if api['name'] == 'dynamo_update':
            return api['id']
    return "No API found with name dynamo_update"

def get_stage(client, api_id):
    stages = client.get_stages(restApiId=api_id)
    return stages['item'][0]['stageName']

def get_resource_id(client, api_id):
    resources = client.get_resources(
        restApiId= api_id
    )
    return resources['items'][0]['id']

def get_api_key(client):
    response = client.get_api_keys()
    if response['items']:
        return response['items'][0]['id']  # return the first API key
    else:
        return None

def post_data():
    client = boto3.client('apigateway', region_name='us-east-1')
    api_name = "dynamo_update"
    api_id = get_rest_api_id(client)
    resource_id = get_resource_id(client, api_id)
    api_key = get_api_key(client)
      # Root resource ('/') ID

    data = {'user': 'newone'}

    # url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/{get_stage(client, api_id)}"

    url = "https://56hajc1j9a.execute-api.us-east-1.amazonaws.com/Prod"

    response = requests.post(url, data=json.dumps(data), headers={"x-api-key": api_key, "Content-Type": "application/json"})

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()

            return super().default(o)

    return json.dumps(response.json(), cls=DateTimeEncoder, indent=4)




if __name__ == "__main__":
    post_data()