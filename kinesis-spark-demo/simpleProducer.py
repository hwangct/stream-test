import time
import json
import requests
#import testdata
from boto import kinesis

#connecting to Kinesis stream
region = 'us-east-1'
kinesisStreamName = 'kinesis-demo'
kinesis = kinesis.connect_to_region(region)
partitionKey = 'shardId-000000000000'

# generating data and feeding kinesis.
while True:
    response = requests.get('https://chasing-coins.com/api/v1/top-coins/20').json()
    for coin in response:
        data = json.dumps(response[coin])
        print data
        result = kinesis.put_record(kinesisStreamName, data, partitionKey)

    time.sleep(0.2)

# class Users(testdata.DictFactory):
#     firstname = testdata.FakeDataFactory('firstName')
#     lastname = testdata.FakeDataFactory('lastName')
#     age = testdata.RandomInteger(10, 30)
#     gender = testdata.RandomSelection(['female', 'male'])

# for user in Users().generate(50):
#     print(user)
#     kinesis.put_record(kinesisStreamName, json.dumps(user), partitionKey)