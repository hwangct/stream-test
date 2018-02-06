import time
import json
import requests
from boto import kinesis


 #connecting to Kinesis stream
region = 'us-east-1'
kinesisStreamName = 'kinesis-spark-demo'
kinesis = kinesis.connect_to_region(region)
partitionKey = 'shardA'

# generating data and feeding kinesis.
#while True:
response = requests.get('https://chasing-coins.com/api/v1/top-coins/20')
data = json.dumps(response.json())

print data

result = kinesis.put_record(kinesisStreamName, data, partitionKey)

#time.sleep(1)